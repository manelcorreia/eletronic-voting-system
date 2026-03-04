from backend import Urna, Caderneta, Pessoa, Candidato, Recenseamento
import os

def menu():
    urna = Urna()
    caderneta = Caderneta()
    recenseamento = Recenseamento()

    if os.path.exists("urnas_fechadas.flag"):
        os.remove("urnas_fechadas.flag")
        print("🔓 Urnas abertas para o dia de eleições!")

    urna.carregar_csv("resultados.csv")
    caderneta.carregar_csv("caderneta.csv")
    recenseamento.carregar_csv("recenseamento.csv")

    while True:
        print("\n--- Controlo da Urna ---")
        print("\n1. Mostrar resultados atuais")
        print("\n2. Encerrar urnas e fechar sistema")
        print("\n3. Verificar erros")
        print("\n0. Sair do programa")

        try:
            option = int(input("Digite a sua opção (1, 2, 3, 4, 5 ou 0): "))

            if option == 1:
                urna.carregar_csv("resultados.csv")
                print("\n--- RESULTADOS PARCIAIS (Sessão Atual) ---")
                resultados_atuais = urna.mostrar_resultados()
                for r in resultados_atuais:
                    print(r)

            elif option == 2:
                print("\nA ENCERRAR SISTEMA E BLOQUEAR TERMINAIS DE VOTO...")

                with open("urnas_fechadas.flag", "w") as f:
                    f.write("FECHADA")

                urna.carregar_csv("resultados.csv")
                print("\n--- RESULTADOS FINAIS OFICIAIS ---")
                resultados_finais = urna.mostrar_resultados()
                for r in resultados_finais:
                    print(r)
                print("\nSistema encerrado.")
                break

            elif option == 3:
                caderneta.carregar_csv("caderneta.csv")
                recenseamento.carregar_csv("recenseamento.csv")

                print("\n--- Verificação de erros ---")
                print("\nQual é o seu erro:")
                print("\nAinda não votei e diz que já votei.")

                opcao = int(input("Digite a sua opção: "))

                if opcao == 1:
                    cc_registados = recenseamento.mostrar_eleitores()
                    for cc in cc_registados:
                        print(cc)

                    cc_perguntado = int(input("Digite o seu cc: "))

                    if recenseamento.verificar_cc(cc_perguntado):
                        print("\nFaz parte da lista, vamos verificar se já votou.")

                        if caderneta.verificar_cc(cc_perguntado):
                            print("\nEstá a dar erro, porque já votou.")

                        else:
                            print("\nAinda não votou e faz parte da lista. Tente novamente e verifique se digita as informações corretamente.")


                    else:
                        print("Está a dar erro, porque não faz parte da lista.")

                else:
                    print("\nOpção inválida.")

            else:
                print("\nOpção inválida.")

        except ValueError:
            print("❌ Erro: Digite um número válido.")

if __name__ == "__main__":
    menu()

