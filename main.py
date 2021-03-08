import sqlite3

def create_tables():
    db = sqlite3.connect("database.db")
    c = db.cursor()
    
    c.execute("""CREATE TABLE IF NOT EXISTS Stock
             (barcode INTERGER PRIMARY KEY, amount INTERGER)""")

    c.execute("""CREATE TABLE IF NOT EXISTS Products
               (barcode INTERGER PRIMARY KEY,name TEXT, price REAL)""")

    db.close()
create_tables()

class Product:
    def __init__(self, barcode, name, price):
        self.barcode = barcode
        self.name = name
        self.price = price

    def add_to_database(self):
        db = sqlite3.connect("database.db")
        c = db.cursor()
    
        c.execute("INSERT INTO Products VALUES(?,?,?)",(self.barcode,self.name,self.price))

        c.execute("INSERT INTO Stock VALUES(?,?)",(self.barcode,1))

        
        db.commit()
        db.close()
    
    def check_stock(self):
        db = sqlite3.connect("database.db")
        c =  db.cursor()
        c.execute(f"SELECT * FROM Stock WHERE barcode = {self.barcode}")
        data = c.fetchall()
        return data[0][1]

p1 = Product(123, "egg", 20.00)
print(p1.check_stock())

def print_all():
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute("SELECT * FROM Products")
    print(c.fetchall())

