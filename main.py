import sqlite3
import barcodenumber
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Column, Integer, String, Float, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import UnmappedInstanceError

engine = create_engine('sqlite:///database.db')
Base = declarative_base()


class Stock(Base):
    __tablename__ = 'stock'
    barcode = Column(Integer, primary_key=True, unique=True)
    quantity = Column(Integer)


class Products(Base):
    __tablename__ = 'products'
    barcode = Column(Integer, primary_key=True, unique=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def barcode_check(barcode):
    return True
    return barcodenumber.check_code("ean13", str(barcode))


def search_database(barcode):
    if barcode_check:
        result = session.query(Products).filter_by(barcode=barcode).first()
        data = [result.barcode, result.name, result.price]
        return data
    return False


class Product:
    def __init__(self, barcode, name, price):
        self.barcode = barcode
        self.name = name
        self.price = price

    def add_to_database(self):
        query = session.query(Products).filter_by(barcode=self.barcode).first()
        if query == None:
            if barcode_check(self.barcode):
                product = Products(barcode=self.barcode, name=self.name, price=self.price)
                session.add(product)
                stock = Stock(barcode=self.barcode, quantity=1)
                session.add(stock)
                session.commit()
                return True
        return False

    def delete_products(self):
        try:
            query = session.query(Products).filter_by(barcode=self.barcode).first()
            session.delete(query)
            query = session.query(Stock).filter_by(barcode=self.barcode).first()
            session.delete(query)
            session.commit()
        except UnmappedInstanceError:
            session.commit()
            return False
        return True

    def check_stock(self):
        query = session.query(Stock).filter_by(barcode=self.barcode).first()
        if query == None:
            return False
        return query.quantity

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


p1 = Product(59134123457, "Milk", 4.00)



#print(search_database(5901234123457))


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
