import sqlite3

def productGetAll():
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute("SELECT * FROM Products")
    dataDump = c.fetchall()
    data = {}
    tempData = {}
    for i in dataDump:
        print(i)
        tempData["name"] = i[1]
        tempData["barcode"] = i[0]
        tempData["price"] = i[2]
        tempData["stock"] = i[3]

        data[i[0]] = tempData
        tempData = {}
    
    print(data)
    print(tempData)

    return data

productGetAll()