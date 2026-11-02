from sqlite3 import IntegrityError

from core.engine import SessionLocal
from repositories.candidato_repository import CandidatoRepository
from repositories.candidatura_repository import CandidaturaRepository
from repositories.pessoa_repository import PessoaRepository
from repositories.urna_repository import UrnaRepository
from services.candidato_service import CandidatoService
from services.candidatura_service import CandidaturaService
from services.pessoa_service import PessoaService
from services.urna_service import UrnaService


def main():
    """Entry point of the program."""
    with SessionLocal() as session:
        candidato_repository = CandidatoRepository(session)
        candidatura_repository = CandidaturaRepository(session)
        urna_repository = UrnaRepository(session)
        pessoa_repository = PessoaRepository(session)
        candidato_service = CandidatoService(session, candidato_repository)
        candidatura_service = CandidaturaService(session, candidatura_repository)
        urna_service = UrnaService(session, urna_repository)
        pessoa_service = PessoaService(session, pessoa_repository)

        while True:
            print("\nBem-Vindo")
            print("1. Iniciar Sessão")
            print("2. Sair")

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
                    pessoa = pessoa_service.iniciar_sessao(cc, password)
                except ValueError as e:
                    print(f"Erro: {e}")

                except IntegrityError as e:
                    print(f"Erro: {e}")

                except Exception as e:
                    print(f"Erro: {e}")

                if not pessoa:
                    continue

                while True:
                    try:
                        candidatos = candidato_service.listar_candidatos()
                        for candidato in candidatos:
                            print(f"{candidato.id} - {candidato.nome}")

                        id_candidato = int(input("Digite o id do candidato que quer votar: "))
                        candidatura_service.adicionar_voto_a_candidatura(pessoa.cc, id_candidato)
                        print("Voto registado com sucesso!")
                        pessoa = None
                        break
                    except ValueError as e:
                        print(f"Erro: {e}")
                    except IntegrityError as e:
                        print(f"Erro: {e}")
                        pessoa = None
                        break
                    except Exception as e:
                        print(f"Erro: {e}")
                        pessoa = None
                        break

            elif opcao == 2:
                print("\nA terminar o programa...")
                break

            else:
                print("Opção inválida. Escolha 1 ou 2.")

if __name__ == "__main__":
    main()