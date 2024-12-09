import sqlite3
import os.path

id_global = 0


def filter_float(pergunta : str) -> float:
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

def filter_int(pergunta : str) -> float:
    while True:
        try:
            value = int(input(pergunta))
            if value <= 0:
                print("Valor precisa ser maior que 0!\n")
                continue
            break
        except:
                print(f"Valor precisa ser um numero inteiro!\n")
                continue
    return int(value)

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

def add_to_db(id : int) -> None:
    nome : str = filter_str("Digite o nome da conta a ser cadastrada: >>")
    valor : float = filter_float(f"Digite o valor de {nome}: >>")
    try:
        db = sqlite3.connect('contas.db')
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO contas VALUES({id},'{nome}',{valor})")
        db.commit()
        db.close()
        print(f"{nome} cadastrado com sucesso!\n")
    except sqlite3.Error as erro:
        print(f"Erro cadastrando {nome}: {erro}")

def remove_key_from_db() -> None:
    global id_global
    id = filter_int("Digite o id da conta a ser removida: >>")
    if id > id_global:
        print("ID nao encontrado no sistema!\n")
        return
    elif filter_str(f"Deseja remover o id de numero: {id}? (S/N): >>") != 's':
        print("Operacao cancelada!\n")
        return
    try:
        db = sqlite3.connect('contas.db')
        cursor = db.cursor()
        cursor.execute(f"DELETE from contas where id = {id}")
        db.commit()
        db.close()
        print(f"conta removida com sucesso!\n")
    except sqlite3.Error as erro:
        print(f"Erro removendo conta: {erro}\n")

def update_keyValue_db() -> None:
    global id_global
    id = filter_int("Digite o id da conta a ser atualizada: >>")
    if id > id_global:
        print("ID nao encontrado no sistema!\n")
        return
    valor = filter_float("Digite o novo valor da conta: >>")
    try:
        db = sqlite3.connect('contas.db')
        cursor = db.cursor()
        cursor.execute(f"UPDATE contas SET valor = '{valor}' WHERE id = '{id}'")
        db.commit()
        db.close()
        print(f"Valor atualizado com sucesso!\n")
    except sqlite3.Error as erro:
        print(f"Erro atualizando valor: {erro}\n")

def update_keyName_db() -> None:
    global id_global
    id = filter_int("Digite o id da conta a ser atualizada: >>")
    if id > id_global:
        print("ID nao encontrado no sistema!\n")
        return
    nome = filter_str("Digite o novo nome da conta: >>")
    try:
        db = sqlite3.connect('contas.db')
        cursor = db.cursor()
        cursor.execute(f"UPDATE contas SET conta = '{nome}' WHERE id = '{id}'")
        db.commit()
        db.close()
        print(f"Nome atualizado com sucesso!\n")
    except sqlite3.Error as erro:
        print(f"Erro atualizando nome: {erro}\n")

def clear_db() -> None:
    try:
        db = sqlite3.connect('contas.db')
        cursor = db.cursor()
        cursor.execute(f"DELETE from contas")
        db.commit()
        db.close()
        print("Dados do sistema limpos com sucesso!\n")
        global id_global
        id_global = 0
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

def load_id():
    temp_dict = retrieve_data_dict()
    id = 0
    for dict in temp_dict:
        if dict['id'] > id:
            id = dict['id']
    global id_global
    id_global = id

def check_db_exist():
    if os.path.isfile("./contas.db"):
        return
    else:
        try:
            db = sqlite3.connect('contas.db')
            cursor = db.cursor()
            cursor.execute(f"CREATE TABLE contas(id int, conta text, valor float)")
            db.commit()
            db.close()
            print(f"DB criado com sucesso!\n")
        except sqlite3.Error as erro:
            print(f"Erro criando db: {erro}\n")

def print_menu():
        line()
        print(" MENU DE CONTAS FIXAS ".center(87, '*'))
        line()
        print("-----|" + f"ID".center(6) + '|' + f"Conta".center(30) + "   |   " + f"Valor".center(31) + "|-----")
        line()
        temp_dict = retrieve_data_dict()
        acum : float = 0.0
        if temp_dict == []:
            print("-----|" + f"----".center(6) + '|' + f"----------".center(30) + "   |   " + f"R$----".center(31) + "|-----")
            line()
            print("-----|" + f"----".center(6) + '|' + f"Valor Total".center(30) + "   |   " + f"R$----".center(31) + "|-----")
            line()
            return
        for dict in temp_dict:
            id = dict['id']
            conta = dict['conta']
            valor = dict['valor']
            acum += valor
            print("-----|" + f"{id}".center(6) + '|' + f"{conta}".center(30) + "   |   " + f"R${valor}".center(31) + "|-----")
        line()
        print("-----|" + f"".center(6) + '|' + f"Valor Total".center(30) + "   |   " + f"R${acum}".center(31) + "|-----")
        line()

def line():
    print('-'.center(87, '-'))

def main() -> None:
    check_db_exist()
    load_id()
    global id_global
    while True:
        print_menu()
        print(" 1. Cadastrar conta\n",
              "2. Atualizar nome da conta\n",
              "3. Atualizar valor da conta\n",
              "4. Deletar conta do sistema\n",
              "5. Apagar todas as contas\n",
              "6. Voltar\n"
              )
        selection = input(">>")
        match selection:
            case '1':
                id_global += 1
                add_to_db(id_global)
            case '2':
                update_keyName_db()
            case '3':
                update_keyValue_db()
            case '4':
                remove_key_from_db()
            case '5':
                if filter_str("Deseja remover todos os dados do sistema? (S/N): ") == 's':
                    if filter_str("Tem certeza? (S/N): ") == 's':
                        if filter_str("Todos os dados serao apagados!!! (S/N): ") == 's':
                            clear_db()
            case '6':
                break

#main
main()