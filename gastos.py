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
    values = list("abcdefghijklmnopqrstuvwxyz ")
    print("O nome nao pode ser maior que 30 caracteres!\n"
            "O nome pode conter apenas letras e numeros!")
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


#add key to db
def add_to_db(key : str, value : float) -> None:
    temp_dict = retrieve_data_dict()
    for k in temp_dict.items():
        if key == k:
            print("Nome ja existe!\n")
            return
    try:
        db = sqlite3.connect('contas.db')
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO contas VALUES('{key}',{value})")
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
                db = sqlite3.connect('contas.db')
                cursor = db.cursor()
                cursor.execute(f"DELETE from contas WHERE conta = '{target_key.lower()}'")
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

#updates a value from db with the new_value value, where the key name is located
def update_keyValue_db(target_key : str) -> None:
    temp_dict = retrieve_data_dict()

    for k, v in temp_dict.items():
        if k == target_key.lower():
            try:
                new_value : float = filter_number(f"Digite o NOVO valor de {target_key}: R$")
                db = sqlite3.connect('contas.db')
                cursor = db.cursor()
                cursor.execute(f"UPDATE contas SET valor = '{new_value}' WHERE conta = '{target_key.lower()}'")
                db.commit()
                db.close()
                print("Valor atualizado com sucesso!\n")
                return
            except sqlite3.Error as erro:
                print(f"Erro atualizando o valor: {erro}\n")
                return
    print(f"{target_key} nao encontrado nos dados :(\n")


#updates a key from db with the new_key value
def update_keyName_db(target_key : str) -> None:
    temp_dict = retrieve_data_dict()

    for k, v in temp_dict.items():
        if k == target_key.lower():
            new_key : str = filter_str("Digite o NOVO nome da conta: ")
            if check_size(new_key):
                try:
                    db = sqlite3.connect('contas.db')
                    cursor = db.cursor()
                    cursor.execute(f"UPDATE contas SET conta = '{new_key}' WHERE conta = '{target_key.lower()}'")
                    db.commit()
                    db.close()
                    print("Nome atualizado com sucesso!!!\n")
                    return
                except sqlite3.Error as erro:
                    print(f"Erro atualizando o nome: {erro}\n")
                    return
            else:
                return
    print(f"{target_key} nao encontrado nos dados :(\n")
    

#retrive raw list, remeber RAW
def retrieve_data_dict():
    temp_dict : dict[str, float] = {}
    try:
        db = sqlite3.connect('contas.db')
        cursor = db.cursor()
        keys = [conta[0] for conta in cursor.execute("SELECT conta FROM contas")]
        values = [valor[0] for valor in cursor.execute("SELECT valor FROM contas")]
        for i in range(0,len(keys)):
            temp_dict[keys[i]] = values[i]
        return temp_dict
    except sqlite3.Error as erro:
        print(f"Erro carregando dados: {erro}\n")

def print_menu():
        temp_dict = retrieve_data_dict()
        line()
        print(" MENU DE contas ".center(80, '*'))
        line()
        print(f"Conta".center(39) + "|" + "Valor".center(39))
        line()
        for k, v in temp_dict.items():
            print("-----|" + f"{k}".rjust(30) + "   |   " + f"R${v:.02f}".ljust(31) + "|-----")
        line()

def line():
    print('-'.center(80, '-'))

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
                nome : str = filter_str("Digite o nome da conta a cadastrar: ")
                if check_size(nome):
                    valor : float = filter_number(f"Digite o valor de {nome}: R$")
                    add_to_db(nome, valor)
            case '2':
                
                update_keyName_db(filter_str("Digite o nome da conta a ser atualizado: "))
            case '3':
                update_keyValue_db(filter_str("Digite o nome da conta para alterar o valor: "))
            case '4':
                nome : str = filter_str("Digite o nome da conta a ser removida: ")
                if filter_str(f"Tem certeza que deseja remover {nome}? (S/N): ") == 's':
                    remove_key_from_db(nome)
            case '5':
                if filter_str("Deseja remover todos os dados do sistema? (S/N): ") == 's':
                    if filter_str("Tem certeza? (S/N): ") == 's':
                        if filter_str("Todos os dados serao apagados!!! (S/N): ") == 's':
                            clear_db()

main()