import sqlite3

#filter numbers
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

#filter strings
def filter_str(pergunta: str) -> str:
    while True:
        string = input(pergunta)
        if type(string) != str:
            print("Nome precisa ser letras!\n")
            continue
        if string == '':
            print("Nome nao pode ficar vazio!\n")
            continue
        break
    return string.lower()

#remove the blanck spaces in beggining and finish 
def remove_initial_last_spaces(string : str) -> str:
    list1 : list = list(string)
    while list1[0] == ' ':
        list1.pop(0)
    while list1[-1] == ' ':
        list1.pop(-1)
    return str(''.join(list1))

#add key to db
def add_to_db(key : str, value : float) -> None:
    key = remove_initial_last_spaces(key)
    temp_dict = retrieve_data_dict()
    for k in temp_dict.items():
        if key == k:
            print("Nome ja existe!\n")
            return
    try:
        db = sqlite3.connect('db_gastos.db')
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO gastos VALUES('{key}',{value})")
        db.commit()
        db.close()
        print("Conta adicionada com sucesso!\n")
    except sqlite3.Error as erro:
        print(f"Erro adicionando conta: {erro}\n")

#remove key from db if found
def remove_key_from_db(target_key : str) -> None:
    temp_dict = retrieve_data_dict()

    for k, v in temp_dict.items():
        if target_key.lower() == k:
            try:
                db = sqlite3.connect('db_gastos.db')
                cursor = db.cursor()
                cursor.execute(f"DELETE from gastos WHERE conta = '{target_key.lower()}'")
                db.commit()
                db.close()
                print("Conta removida com sucesso!\n")
                return
            except sqlite3.Error as erro:
                print(f"Erro removendo conta: {erro}\n")
                return
    print("Nome nao encontrado nos dados :(\n")
            

#clear de database
def clear_db() -> None:
    try:
        db = sqlite3.connect('db_gastos.db')
        cursor = db.cursor()
        cursor.execute(f"DELETE from gastos")
        db.commit()
        db.close()
        print("Dados limpos com sucesso!\n")
        return
    except sqlite3.Error as erro:
        print(f"Erro ao limpar dados: {erro}\n")
        return

#updates a value from db with the new_value value, where the key name is located
def update_keyValue_db(target_key : str) -> None:
    temp_dict = retrieve_data_dict()

    for k, v in temp_dict.items():
        if k == target_key.lower():
            try:
                new_value : float = filter_number("Digite o NOVO valor da conta: R$")
                db = sqlite3.connect('db_gastos.db')
                cursor = db.cursor()
                cursor.execute(f"UPDATE gastos SET valor = '{new_value}' WHERE conta = '{target_key.lower()}'")
                db.commit()
                db.close()
                print("Valor atualizado com sucesso!\n")
                return
            except sqlite3.Error as erro:
                print(f"Erro atualizando o valor: {erro}\n")
                return
    print("Nome nao encontrado nos dados :(\n")


#updates a key from db with the new_key value
def update_keyName_db(target_key : str) -> None:
    temp_dict = retrieve_data_dict()
    print(temp_dict)

    for k, v in temp_dict.items():
        if k == target_key.lower():
            new_key : str = filter_str("Digite o NOVO nome da conta: ")
            try:
                db = sqlite3.connect('db_gastos.db')
                cursor = db.cursor()
                cursor.execute(f"UPDATE gastos SET conta = '{new_key}' WHERE conta = '{target_key.lower()}'")
                db.commit()
                db.close()
                print("Nome atualizado com sucesso!!!\n")
                return
            except sqlite3.Error as erro:
                print(f"Erro atualizando o nome: {erro}\n")
                return
    print("Nome nao encontrado nos dados :(\n")
    

#retrive raw list, remeber RAW
def retrieve_data_dict():
    temp_dict : dict[str, float] = {}
    try:
        db = sqlite3.connect('db_gastos.db')
        cursor = db.cursor()
        keys = [conta[0] for conta in cursor.execute("SELECT conta FROM gastos")]
        values = [valor[0] for valor in cursor.execute("SELECT valor FROM gastos")]
        for i in range(0,len(keys)):
            temp_dict[keys[i]] = values[i]
        print("Dados carrergados com sucesso!\n")
        return temp_dict
    except sqlite3.Error as erro:
        print(f"Erro carregando dados: {erro}\n")

def print_menu():
        temp_dict = retrieve_data_dict()
        line()
        print(" MENU DE GASTOS ".center(80, '*'))
        line()
        print(f"Conta".center(39) + "|" + "Valor".center(39))
        line()
        for k, v in temp_dict.items():
            print("-----|" + f"{k}".center(33) + "|             " + f"R${v:.02f}".ljust(21) + "|-----")
        line()

def line():
    print('-'.center(80, '-'))

def main() -> None:
    while True:
        print_menu()
        print(" 1. Cadastrar conta\n",
              "2. Atualizar nome da conta\n",
              "3. Atualizar valor da conta\n",

              )
        selection = input(">>").lower()
        match selection:
            case '1':
                add_to_db(filter_str("Digite o nome da conta: "), filter_number("Digite o valor da conta: R$"))
            case '2':
                update_keyName_db(filter_str("Digite o nome da conta: "))
            case '3':
                break










add_to_db('testa', 11111111)

main()