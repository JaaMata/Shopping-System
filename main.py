import sqlite3
import barcodenumber


def create_tables():
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS Stock
             (barcode INTEGER PRIMARY KEY, amount INTEGER)""")

    c.execute("""CREATE TABLE IF NOT EXISTS Products
               (barcode INTEGER PRIMARY KEY,name TEXT, price REAL)""")
    db.close()


create_tables()


def check_sum(barcode):
    return barcodenumber.check_code("ean13", str(barcode))


def search_database(barcode):
    if check_sum(barcode):
        db = sqlite3.connect("database.db")
        c = db.cursor()
        c.execute(f"SELECT * FROM Products WHERE barcode = {barcode}")
        data = c.fetchall()
        return data
    return False


class Product:
    def __init__(self, barcode, name, price):
        self.barcode = barcode
        self.name = name
        self.price = price

    def add_to_database(self):
        if check_sum(self.barcode):
            db = sqlite3.connect("database.db")
            c = db.cursor()

            c.execute("INSERT INTO Products VALUES(?,?,?)", (self.barcode, self.name, self.price))
            c.execute("INSERT INTO Stock VALUES(?,?)", (self.barcode, 1))

            db.commit()
            db.close()
        return False

    def delete_products(self):
        db = sqlite3.connect("database.db")
        c = db.cursor()
        c.execute(f"DELETE FROM Products WHERE barcode = {self.barcode}")
        c.execute(f"DELETE FROM Stock WHERE barcode = {self.barcode}")
        db.commit()
        db.close()

    def check_stock(self):
        db = sqlite3.connect("database.db")
        c = db.cursor()
        c.execute(f"SELECT * FROM Stock WHERE barcode = {self.barcode}")
        data = c.fetchall()
        return int(data[0][1])

    def set_stock(self, amount):
        db = sqlite3.connect("database.db")
        c = db.cursor()
        c.execute(f"UPDATE Stock SET amount = {amount} WHERE barcode = {self.barcode}")
        c.execute(f"SELECT * FROM Stock WHERE barcode = {self.barcode}")
        data = c.fetchall()
        db.commit()
        db.close()
        if data[0][1] == amount:
            return True
        return False

    def increase_stock(self, increase_amount):
        amount = self.check_stock()
        db = sqlite3.connect("database.db")
        c = db.cursor()
        c.execute(f"UPDATE Stock SET amount = {amount + increase_amount} WHERE barcode = {self.barcode}")
        c.execute(f"SELECT * FROM Stock WHERE barcode = {self.barcode}")
        data = c.fetchall()
        db.commit()
        db.close()
        if data[0][1] == amount + increase_amount:
            return True
        return False

    def decrease_stock(self, decreasing_amount):
        amount = self.check_stock()
        if amount - decreasing_amount < 0:
            amount, decreasing_amount = 0, 0
        db = sqlite3.connect("database.db")
        c = db.cursor()
        c.execute(f"UPDATE Stock SET amount = {amount - decreasing_amount} WHERE barcode = {self.barcode}")
        c.execute(f"SELECT * FROM Stock WHERE barcode = {self.barcode}")
        db.commit()
        db.close()


# p1 = Product(5901234123457, "eggs", 2.00)

# print(p1.decrease_stock(17))

# print(p1.increase_stock(17))

def print_all():
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute("SELECT * FROM Products")
    print(c.fetchall())
    c.execute("SELECT * FROM Stock")
    print(c.fetchall())

print_all()