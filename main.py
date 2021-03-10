import sqlite3
import barcodenumber
from sqlalchemy import Column, Integer, String, Float
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
        query = session.query(Products).filter_by(barcode=barcode).first()
        data = [query.barcode, query.name, query.price]
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

    def rename_barcode(self, new_barcode):
        query = session.query(Products).filter_by(barcode=self.barcode).first()
        query.barcode = new_barcode
        session.commit()

    def rename_product(self, new_name):
        query = session.query(Products).filter_by(barcode=self.barcode).first()
        query.name = new_name
        session.commit()

    def new_price(self, new_price):
        query = session.query(Products).filter_by(barcode=self.barcode).first()
        query.price = new_price
        session.commit()

    def check_stock(self):
        query = session.query(Stock).filter_by(barcode=self.barcode).first()
        if query == None:
            return False
        return query.quantity

    def set_stock(self, amount):
        query = session.query(Stock).filter_by(barcode=self.barcode).first()
        query.quantity = amount
        session.commit()

    def increase_stock(self, increase_amount):
        query = session.query(Stock).filter_by(barcode=self.barcode).first()
        query.quantity = query.quantity + increase_amount
        session.commit()

    def decrease_stock(self, decreasing_amount):
        query = session.query(Stock).filter_by(barcode=self.barcode).first()
        query.quantity = query.quantity - decreasing_amount
        if query.quantity < 0:
            query.quantity = 0
        session.commit()

p1 = Product(59134123457, "Milk", 4.00)

# print(search_database(5901234123457))

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


def genorate_barcode():
    pass
