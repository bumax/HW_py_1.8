# Задача 49 Создать телефонный справочник с возможностью импорта и экспорта данных в формате .txt. 
# Фамилия, имя, отчество, номер телефона - данные, которые должны находится в файле. Дополнить телефонный справочник 
# возможностью изменения и удаления данных. Пользователь также может ввести имя или фамилию, и Вы должны реализовать 
# функционал для изменения и удаления данных


# ---------------------------------------- !!! НАЧАЛО: ФУНКЦИИ !!! ---------------------------------------
# Загрузка базы данных, модель состоит из двух элементов: первый - это номер строки в файле, второй - распарсеный список с данными
def load_db(path):
    data = open(path, 'r')
    db = []
    line_number = 0
    for line in data:
        csv_parse = line.replace("\n","").split(';')
        db.append([line_number,csv_parse])
        line_number += 1
    data.close()
    return db

# Функция поиска ID пользователя
def find_id(database, first_name = "", last_name = ""): # имя, фамилия
    # по умолчанию, если нет результата, возвращеем индекс -1
    find_id = -1
    # 3 варианта поиска:по имени И фамилии, по имени, по фамилии. Функция возвращает первое совпадение.
    # TODO: сделать возможность выбирать из нескольких совпадений 
    if first_name != "" and last_name != "": # по имени И фамилии
        res = list(filter(lambda x: x[1][1].lower() == first_name.lower() and x[1][0].lower() == last_name.lower(), database))
        if len(res) > 0:
            find_id = res[0][0]
    elif(first_name != ""): # по имени
        res = list(filter(lambda x: x[1][1].lower() == first_name.lower(), database))
        if len(res) > 0:
            find_id = res[0][0]
    elif(last_name != ""): # по фамилии
        res = list(filter(lambda x: x[1][0].lower() == last_name.lower(), database))
        if len(res) > 0:
            find_id = res[0][0]       
    return find_id

def find_phone(database, id):
    if id == -1:
        print("Абонент не абонент!")
    else:
        print(database[id][1], sep="\t")

def delete_phone(path, database, id):
    if id != -1:
        database.pop(id)
        data = open(path, 'w')
        for db in database:
            data.writelines([x + ";" if i < 3 else x + "\n" for i,x in enumerate(db[1])])
        data.close()

def edit_user(path, database, id, new_data):
    if id != -1:
        # Если какая то строка пустая, оставляем старые значения
        new_data[0] = new_data[0] if new_data[0] != "" else database[id][1][0]
        new_data[1] = new_data[1] if new_data[1] != "" else database[id][1][1]
        new_data[2] = new_data[2] if new_data[2] != "" else database[id][1][2]
        new_data[3] = new_data[3] if new_data[3] != "" else database[id][1][3]
        database[id][1] = new_data
        db = list(zip(database))
        data = open(path, 'w')
        for db in database:
            data.writelines([x + ";" if i < 3 else x + "\n" for i,x in enumerate(db[1])])
        data.close()

# ---------------------------------------- !!! КОНЕЦ: ФУНКЦИИ !!! ---------------------------------------
 

# Путь к БД
db_path = "database.csv"

# Загружаем БД
db = load_db(db_path)

# Инициализируем команду (1 - поиск абонента)
cmd = 1
# Результат текущего поиска (-1 - абонент не найден)
current_uid = -1

# Пока команда больше 0, держим диалог
while(cmd > 0):
     
    if cmd == 1: # Поиск абонента
        l_n = input("Поиск абонента, введите фамилию или оставте поле пустым: ")
        f_n = input("Поиск абонента, введите имя или оставте поле пустым: ")
        current_uid = find_id(db, f_n, l_n)
        find_phone(db, current_uid)
        cmd = int(input("1 - повторить поиск, 2 - удалить, 3 - изменить, 0 - выход: "))
    elif cmd == 2: # Удаление абонента
        delete_phone(db_path, db, current_uid)
        db = load_db(db_path)
        cmd = 1
    elif cmd == 3: # Изменение данных абонента
        l_n = input("Введите фамилию абонента или оставте поле пустым: ")
        f_n = input("Введите имя абонента или оставте поле пустым: ")
        s_n = input("Введите отчество абонентаили оставте поле пустым: ")
        p_n = input("Введите телефон абонента или оставте поле пустым: ")        
        edit_user(db_path, db, current_uid, [l_n,f_n,s_n,p_n])
        cmd = 1
    else: # Если пришла неизвестная команда, то возвращаемся к поиску
        cmd = 1