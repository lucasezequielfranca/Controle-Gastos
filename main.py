import contas_fixas
from contas_fixas import line as line
print("Programa desenvolvido por Lucas Franca\n")
print('Toda honra para Deus e Jesus Cristo\n')
while True:
        line()
        print(" Sistema de Controle de Financeiro ".center(87, '*'))
        line()
        print(" 1. Menu Contas Fixas\n",
              "5. Encerrar o sistema\n"
              )
        selection = input(">>")
        match selection:
            case '1':
                contas_fixas.main()
            case '5':
                  exit()