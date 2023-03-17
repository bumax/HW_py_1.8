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
