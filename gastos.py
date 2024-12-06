import sqlite3

def add_to_db(key : str, value : float) -> None:
    try:
        db = sqlite3.connect('db_gastos.db')
        cursor = db.cursor()

        if type(key) != str:
            print("Key must be string!")
            return 1
        if key == '':
            print("Key cant't be empty!")
            return 1
        if type(value) != float and type(value) != int:
            print("Value must be a number!")
            return 2
        if value <= 0:
            print("Value can't be less than 0.01!")
            return 2
        cursor.execute(f"INSERT INTO gastos VALUES('{key}',{value})")
        db.commit()
        db.close()
        print("Data added to db with sucess!")
    except sqlite3.Error as erro:
        print(f"Error when adding data: {erro}")

def remove_key_from_db(key : str) -> None:
    try:
        db = sqlite3.connect('db_gastos.db')
        cursor = db.cursor()

        if type(key) != str:
            print("Key must be string!")
            return 1
        if key == '':
            print("Key cant't be empty!")
            return 1
        cursor.execute(f"DELETE from gastos WHERE conta = '{key}'")
        db.commit()
        db.close()
        print("Data removed from db with sucess!")
    except sqlite3.Error as erro:
        print(f"Error when removing data: {erro}")

def clear_db() -> None:
    try:
        db = sqlite3.connect('db_gastos.db')
        cursor = db.cursor()
        cursor.execute(f"DELETE from gastos")
        db.commit()
        db.close()
        print("Data cleared with sucess!")
    except sqlite3.Error as erro:
        print(f"Error when cleaning data: {erro}")

def update_keyValue_db(target_key : str, new_value : float) -> None:
    try:
        db = sqlite3.connect('db_gastos.db')
        cursor = db.cursor()

        if type(target_key) != str:
            print("Key must be string!")
            return 1
        if target_key == '':
            print("Key cant't be empty!")
            return 1
        if type(new_value) != float and type(new_value) != int:
            print("Value must be a number!")
            return 2
        if new_value <= 0:
            print("Value can't be less than 0.01!")
            return 2
        cursor.execute(f"UPDATE gastos SET valor = {new_value} WHERE conta = '{target_key}'")
        db.commit()
        db.close()
        print("Key value updated with sucess!")
    except sqlite3.Error as erro:
        print(f"Error updating Key value: {erro}")

def update_keyName_db(target_key : str, new_key : float) -> None:
    temp_dict = retrieve_data_dict()
    try:
        for k, v in temp_dict;
            if k == target_key:
                
        db = sqlite3.connect('db_gastos.db')
        cursor = db.cursor()

        if type(target_key) != str:
            print("Key must be string!")
            return 1
        if target_key == '':
            print("Key cant't be empty!")
            return 1
        if type(new_key) != str:
            print("NewKey must be string!")
            return 2
        if new_key == '':
            print("NewKey cant't be empty!")
            return 1
        cursor.execute(f"UPDATE gastos SET conta = '{new_key}' WHERE conta = '{target_key}'")
        db.commit()
        db.close()
        print("KeyName updated with sucess!")
    except sqlite3.Error as erro:
        print(f"Error updating KeyName value: {erro}")

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
        print("Data retrieved with sucess!")
        return temp_dict
    except sqlite3.Error as erro:
        print(f"Error when retriving data: {erro}")

remove_key_from_db('test')
update_keyName_db('aluguel', casa)
print(retrieve_data_dict())