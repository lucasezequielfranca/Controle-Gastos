import menu_contas_fixas
import menu_dia_detalhado
from calendar import monthrange
from datetime import datetime
from funcoes import *
import sqlite3
import os.path

current_month : int = int(datetime.today().strftime('%m'))
current_day : int = int(datetime.today().strftime('%d'))
current_year : int = int(datetime.today().strftime('%Y'))
month_range_tupple : int = monthrange(current_year, current_month)
month_range : int = int(month_range_tupple[1])



print("Programa desenvolvido por Lucas Franca\n")
print('Toda honra para Deus e Jesus Cristo\n')
while True:
        linha()
        print(" Sistema de Controle de Financeiro ".center(87, '*'))
        linha()
        print(" 1. Menu do Dia\n",
              "2. Acessar outro Dia\n",
              "3. Menu Contas fixas\n"
              " 5. Encerrar o sistema\n"
              )
        selection = input(">>")
        match selection:
            case '1':
                menu_dia_detalhado.main(current_day, current_month, current_year, month_range)
            case '2':
                pass
            case '3':
                  menu_contas_fixas.main()
            case '5':
                  exit()