import datetime
import sqlite3

import main

today = datetime.datetime.today()
date = today.strftime("%Y/%m/%d %H:%M:%S")

global depot
global logs
global sql
global sqlLog
depot = sqlite3.connect('server.depot')
logs = sqlite3.connect('server.logs')
sql = depot.cursor()
sqlLog = logs.cursor()

sql.execute("CREATE TABLE IF NOT EXISTS depot (id INT, item TEXT, price FLOAT, quantity INT, date_added TEXT)")
depot.commit()

sqlLog.execute("CREATE TABLE IF NOT EXISTS logs (id INT, status TEXT, quantity INT, date_added TEXT)")
logs.commit()


def addItem():
    _id = input('Bar code: ')
    item_name = input('Name: ')
    item_price = input('Price: ')
    quantity: int = input('Quantity: ')
    add = 'Added'

    sql.execute(f"SELECT id FROM depot WHERE id = '{_id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO depot VALUES (?, ?, ?, ?, ?)", (_id, item_name, item_price, quantity, date))
        sqlLog.execute(f"INSERT INTO logs VALUES (?, ?, ?, ?)", (_id, add, quantity, date))
        depot.commit()
        logs.commit()
        main.main()
    else:
        print('Item already exists in system. Please enter how much will be added.')
        addQuantity()


def delItem():
    _id = input('Bar code: ')
    dell = 'Removed'

    sql.execute(f"SELECT id FROM depot WHERE id = '{_id}'")
    if sql.fetchone() is None:
        print('No such item.')
        main.main()
    else:
        wasQuantity = sqlLog.execute(f"SELECT quantity FROM logs").fetchone()[0]
        sql.execute(f"DELETE FROM depot WHERE id = '{_id}'")
        sqlLog.execute(f"INSERT INTO logs VALUES (?, ?, ?, ?)", (_id, dell, int(wasQuantity), date))
        depot.commit()
        logs.commit()


def addQuantity():
    _id: int = input('Bar code: ')
    newQuantity: int = input('Quantity: ')
    add = 'Added'

    sql.execute(f"SELECT id FROM depot WHERE id = '{_id}'")
    if sql.fetchone() is None:
        print('No such item found. Do you want to add new?')
        ask = input('Y/N: ')
        if ask == 'Y' or ask == 'yes' or ask == 'y' or ask == 'Yes' or ask == 'YES':
            addItem()
        elif ask == 'N' or ask == 'no' or ask == 'n' or ask == 'No' or ask == 'NO':
            main.main()
    else:
        oldQuantity = sql.execute(f"SELECT quantity FROM depot").fetchone()[0]
        sql.execute(f"UPDATE depot SET quantity = '{int(oldQuantity) + int(newQuantity)}' WHERE id = '{_id}'")
        sqlLog.execute(f"INSERT INTO logs VALUES (?, ?, ?, ?)", (_id, add, int(newQuantity), date))
        depot.commit()
        logs.commit()


def delQuantity():
    _id = input('Bar code:')
    newQuantity = int(input('Quantity: '))
    dell = 'Removed'

    sql.execute(f"SELECT id FROM depot WHERE id = '{_id}'")
    if sql.fetchone() is None:
        print('No such item found.')
    else:
        oldQuantity = sql.execute(f"SELECT quantity FROM depot").fetchone()[0]
        sql.execute(f"UPDATE depot SET quantity = '{int(oldQuantity) - int(newQuantity)}' WHERE id = '{_id}'")
        sqlLog.execute(f"INSERT INTO logs VALUES (?, ?, ?, ?)", (_id, dell, int(newQuantity), date))
        depot.commit()
        logs.commit()


def showDepot():
    print('-------------- Depot --------------')
    print("Bar code | Item name | Price | Quantity | Date and time")
    for value in sql.execute("SELECT * FROM depot"):
        print(value)


def showLog():
    print('-------------- Log --------------')
    print("Bar code | Status | Quantity | Date and time")
    for value in sqlLog.execute("SELECT * FROM logs"):
        print(value)
