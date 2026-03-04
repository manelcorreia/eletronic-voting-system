from backend import Urna, Caderneta, Pessoa, Candidato, Recenseamento
import os
import time

def main():
    urna = Urna()
    caderneta = Caderneta()
    recenseamento = Recenseamento()


    while True:
        if os.path.exists("urnas_fechadas.flag"):
            print("\n" + "🛑" * 20)
            print("AS URNAS FORAM ENCERRADAS PELO PRESIDENTE DA MESA.")
            print("O processo eleitoral terminou. Obrigado.")
            print("🛑" * 20)
            time.sleep(3)  # Pausa de 3 segundos
            break  # Desliga este programa automaticamente!

        urna.carregar_csv("resultados.csv")
        caderneta.carregar_csv("caderneta.csv")
        recenseamento.carregar_csv("recenseamento.csv")

        print("\n" + "=" * 40)
        print("🗳️  SISTEMA ELEITORAL CENTRAL 🗳️")
        print("=" * 40)
        print("1. Registar novo Voto")
        print("=" * 40)

        op = int(input("Opção: "))

        if op == 1:
            print("\n" + "=" * 40)
            print("🗳️  Verificar se pode votar  🗳️")
            print("=" * 40)

            try:
                nome = input("Digite o nome do eleitor: ")
                cc = int(input("Digite o CC: "))

                if recenseamento.verificar_cc(cc):
                    print("Tudo certo. Pode votar...")

                else:
                    print("Não faz parte da lista. Não pode votar...")
                    continue

                print("\n--- REGISTO DE ELEITOR ---")

                if caderneta.verificar_cc(cc):
                    print("\nJá votou. Não pode votar mais que 1 vez.")
                else:
                    voto = input("Voto: ")

                    certeza = input("Tem a certeza do seu voto? [s, n] ")
                    if certeza == "s":

                        # menu manda a urna processar o voto
                        sucesso, mensagem = urna.votar(voto)
                        print(f"{mensagem}")

                        # guardar a pessoa na caderneta
                        nova_pessoa = Pessoa(nome, cc)
                        caderneta.adicionar_votante(nova_pessoa)

                        urna.to_csv("resultados.csv")
                        caderneta.pessoa_to_csv("caderneta.csv")
                        print("Voto guardado automaticamente no sistema (base de dados).")

                    if certeza == "n":
                        continue

            except ValueError:
                print("Erro: O CC tem de ser um número.")

        else:
            print("Opção inválida. Tente novamente digitar o número 1.")


if __name__ == "__main__":
    main()
