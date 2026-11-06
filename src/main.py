from sqlalchemy.exc import IntegrityError

from core.engine import SessionLocal
from repositories.candidato_repository import CandidatoRepository
from repositories.candidatura_repository import CandidaturaRepository
from repositories.pessoa_repository import PessoaRepository
from repositories.urna_repository import UrnaRepository
from services.candidato_service import CandidatoService
from services.candidatura_service import CandidaturaService
from services.pessoa_service import PessoaService
from services.urna_service import UrnaService

def selecionar_urna(urna_service: UrnaService):
    """Permite ao admin escolher a urna que vai estar disponivel para votar"""
    while True:
        try:
            urnas = urna_service.mostrar_todas_urnas()
            if not urnas:
                print("Não existem urnas registadas no sistema.")
                return None

            print("\n--- Selecionar Urna ---")
            for u in urnas:
                print(f"{u.id} - {u.localidade}")


            opcao = int(input("Selecione o id: "))
            urna = urna_service.obter_urna_por_id(opcao)
            return urna
        except ValueError:
            print("Opção tem de ser um número inteiro.")
            continue
        except IntegrityError as e:
            print(f"Erro: {e}")
            continue
        except Exception as e:
            print(f"Erro: {e}")
            continue

def main():
    """Entry point of the program."""
    with SessionLocal() as session:
        candidato_repository = CandidatoRepository(session)
        candidatura_repository = CandidaturaRepository(session)
        urna_repository = UrnaRepository(session)
        pessoa_repository = PessoaRepository(session)
        candidato_service = CandidatoService(session, candidato_repository, urna_repository, candidatura_repository)
        candidatura_service = CandidaturaService(session, candidatura_repository)
        urna_service = UrnaService(session, urna_repository, candidatura_repository, candidato_repository, pessoa_repository)
        pessoa_service = PessoaService(session, pessoa_repository)

        urna_id = None
        admin = None

        while True:
            print("\n==============================")
            print("   SISTEMA DE VOTAÇÃO DIGITAL  ")
            print("==============================")
            print("1. Iniciar Sessão (Administração)")
            print("2. Encerrar Sistema (Contar votos e ver estatísticas)")

            try:
                opcao = int(input("Opção (1 a 2): "))
            except ValueError:
                print("Opção tem de ser um número inteiro entre 1 e 2")
                continue

            if opcao == 1:
                try:
                    cc = input("\nDigite o seu cc: ")
                    password = input("\nDigite sua senha: ")
                    admin = pessoa_service.iniciar_sessao_admin(cc, password)
                except ValueError as e:
                    print(f"Erro: {e}")
                    continue

                except IntegrityError as e:
                    print(f"Erro: {e}")
                    continue

                except Exception as e:
                    print(f"Erro: {e}")
                    continue

                if not admin:
                    continue

                urna_ativa = selecionar_urna(urna_service)
                if not urna_ativa:
                    print("Nenhuma urna selecionada. A voltar ao menu inicial...")
                    continue

                print(f"\n>>> Tudo pronto para votação na urna: [{urna_ativa.id}] {urna_ativa.localidade} <<<")

                while True:
                    print(f"\nBem-Vindo à urna digital {urna_ativa.localidade}")
                    print("1. Autenticar")
                    print("2. Fechar Urna e Sair")

                    try:
                        opcao = int(input("Opção (1 a 2): "))
                    except ValueError:
                        print("Opção tem de ser um número inteiro entre 1 e 2")
                        continue

                    if opcao == 1:
                        pessoa = None
                        try:
                            cc = input("\nDigite o seu cc: ")
                            password = input("\nDigite sua senha: ")
                            pessoa = pessoa_service.iniciar_sessao(cc, password, urna_ativa)
                        except ValueError as e:
                            print(f"Erro: {e}")
                            continue
                        except IntegrityError as e:
                            print(f"Erro: {e}")
                            continue
                        except Exception as e:
                            print(f"Erro: {e}")
                            continue

                        for candidato in candidato_service.listar_candidatos():
                            print(f"{candidato.id} - {candidato.nome}")

                        try:
                            voto = int(input("Id do candidato a votar: "))
                            candidatura_service.votar(pessoa, voto)
                            print(f"Voto com sucesso!")
                        except ValueError:
                            print("ID tem de ser um número inteiro")
                            continue
                        except IntegrityError as e:
                            print(f"Erro: {e}")
                            continue
                        except Exception as e:
                            print(f"Erro: {e}")
                            continue

                    elif opcao == 2:
                        cc_responsavel = input("\nDigite o seu cc: ")
                        password_responsavel = input("\nDigite sua senha: ")
                        if pessoa_service.confirmar_responsavel(cc_responsavel, password_responsavel):
                            print("Sucesso! A fechar urna...")
                            break

            elif opcao == 2:
                print("\nA terminar o programa...")
                urna_service.fechar_urna(admin, urna_ativa.id)
                totais = candidatura_service.ver_votos_totais_urna(urna_ativa.id)
                numero_pessoas_votaram = urna_service.ver_quantos_votaram(urna_ativa.id)
                numero_pessoas_nao_votaram = urna_service.ver_quantos_nao_votaram(urna_ativa.id)
                abstencao = urna_service.ver_abstencao(urna_ativa.id)
                print(f"\nTotal de votos nesta urna: {totais}")
                print(f"Total de pessoas que votaram: {numero_pessoas_votaram}")
                print(f"Total de pessoas que não votaram: {numero_pessoas_nao_votaram}")
                print(f"Abstenção: {abstencao}%")
                break

            else:
                print("Opção inválida. Escolha 1 ou 2.")

if __name__ == "__main__":
    main()