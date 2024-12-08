import sqlite3

global_id : int = 0

def filter_number(pergunta : str) -> float:
    while True:
        try:
            value = float(input(pergunta))
            if value <= 0:
                print("Valor precisa ser maior que 0.01!\n")
                continue
            break
        except:
                print(f"Valor precisa ser um numero!\n")
                continue
    return float(value)

def filter_str(pergunta: str) -> str:
    values = list("abcdefghijklmnopqrstuvwxyz ")
    while True:
        my_string = input(pergunta).lower()
        if my_string == '':
            print("Nome nao pode ficar em branco\n")
            continue
        for item in my_string:
            if item not in values:
                my_string = my_string.replace(item, "")
        list1 : list = list(my_string)
        while list1[0] == ' ':
            list1.pop(0)
        while list1[-1] == ' ':
            list1.pop(-1)
        if len(list1) > 30:
            print("O nome nao pode ser maior que 30 caracteres\n"
                  "Removendo caracteres excedentes!")
        while len(list1) > 30:
            list1.pop(-1)
        my_string = str(''.join(list1))
        break
    return my_string

def add_to_db(id : int, key : str, value : float) -> None:
    pass

def remove_key_from_db(id : int) -> None:
    pass

def update_keyValue_db(target_key : str) -> None:
    pass

def update_keyName_db(target_key : str) -> None:
    pass

def clear_db() -> None:
    try:
        db = sqlite3.connect('contas.db')
        cursor = db.cursor()
        cursor.execute(f"DELETE from contas")
        db.commit()
        db.close()
        print("Dados limpos com sucesso!\n")
        return
    except sqlite3.Error as erro:
        print(f"Erro ao limpar dados: {erro}\n")
        return

def retrieve_data_dict():
    temp_dict : list[dict[str, float]] = {}
    try:
        cur = sqlite3.connect('contas.db').cursor()
        query = cur.execute('SELECT * FROM contas')
        colname = [ d[0] for d in query.description ]
        temp_dict = [ dict(zip(colname, r)) for r in query.fetchall() ]
        cur.close()
        cur.connection.close()
        return temp_dict
    except sqlite3.Error as erro:
        print(f"Erro carregando dados: {erro}\n")

def print_menu():
        line()
        print(" MENU DE CONTAS ".center(87, '*'))
        line()
        print("-----|" + f"ID".center(6) + '|' + f"Conta".center(30) + "   |   " + f"Valor".center(31) + "|-----")
        line()
        temp_dict = retrieve_data_dict()
        for dict in temp_dict:
            id = dict['id']
            conta = dict['conta']
            valor = dict['valor']
            print("-----|" + f"{id}".center(6) + '|' + f"{conta}".center(30) + "   |   " + f"R${valor}".center(31) + "|-----")
        line()

def line():
    print('-'.center(87, '-'))

def main() -> None:
    while True:
        print_menu()
        print(" 1. Cadastrar conta\n",
              "2. Atualizar nome da conta\n",
              "3. Atualizar valor da conta\n",
              "4. Deletar conta do sistema\n",
              "5. Remover todas as contas\n",
              )
        selection = input(">>").lower()
        match selection:
            case '1':
                pass
            case '2':
                pass
            case '3':
                pass
            case '4':
                pass
            case '5':
                if filter_str("Deseja remover todos os dados do sistema? (S/N): ") == 's':
                    if filter_str("Tem certeza? (S/N): ") == 's':
                        if filter_str("Todos os dados serao apagados!!! (S/N): ") == 's':
                            clear_db()





main()