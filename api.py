from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from threading import Thread
import sqlite3
import barcodenumber
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import UnmappedInstanceError

engine = create_engine('sqlite:///database.db')
Base = declarative_base()


class Products(Base):
    __tablename__ = 'products'
    barcode = Column(Integer, primary_key=True, unique=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def barcode_check(barcode):
    if barcodenumber.check_code("ean13", str(barcode)):
        return True
    return False


def search_database(barcode):
    if barcode_check(barcode):
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(Products).filter_by(barcode=barcode).first()
        if query == None:
            return False
        data = {"barcode": query.barcode, "name": query.name, "price": query.price}
        session.close()
        return data
    return False


class Product:
    def __init__(self, barcode, name, price, quantity):
        self.barcode = barcode
        self.name = name
        self.price = price
        self.quantity = quantity

    def add_to_database(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(Products).filter_by(barcode=self.barcode).first()
        if query == None:
            if barcode_check(self.barcode):
                product = Products(barcode=self.barcode, name=self.name, price=self.price, quantity=self.quantity)
                session.add(product)
                session.commit()
                session.close()
                return True
        session.close()
        return False

def delete_products(barcode):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(Products).filter_by(barcode=barcode).first()
        session.delete(query)
        session.commit()
    except UnmappedInstanceError:
        session.commit()
        session.close()
        return False
    session.close()
    return True

def rename_barcode(barcode, new_barcode):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Products).filter_by(barcode=barcode).first()
    query.barcode = new_barcode
    session.commit()
    session.close()

def rename_product(barcode, new_name):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Products).filter_by(barcode=barcode).first()
    query.name = new_name
    session.commit()
    session.close()

def new_price(barcode, new_price):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Products).filter_by(barcode=barcode).first()
    query.price = new_price
    session.commit()
    session.close()

def check_stock(barcode):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Products).filter_by(barcode=barcode).first()
    session.close()
    if query == None:
        return False
    data = {"quantity" : query.quantity}
    return data


def set_stock(barcode, amount):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Products).filter_by(barcode=barcode).first()
    query.quantity = amount
    session.commit()
    session.close()

def increase_stock(barcode, increase_amount):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Products).filter_by(barcode=barcode).first()
    query.quantity = query.quantity + increase_amount
    session.commit()
    session.close()

def decrease_stock(barcode, decreasing_amount):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Products).filter_by(barcode=barcode).first()
    query.quantity = query.quantity - decreasing_amount
    if query.quantity < 0:
        query.quantity = 0
    session.commit()
    session.close()

barcodes = []
names = ["Eggs", "Milk", "Bread", "Ice cream", "Flour", "Tea Bags", "Rat Poison", "Chocolate", "", ""]
prices = [4.50, 3.25, 6.42, 10.00, 3.00, 2.40, 0.99, 4.30, 5.00,6.00]


#for i in range(10):
#    
p1 = Product(5901234123457, "Milk", 4.00, 3)


# print(search_database(5901234123457))

# print(p1.decrease_stock(17))

# print(p1.increase_stock(17))

def product_get_all():
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute("SELECT * FROM Products")
    dataDump = c.fetchall()
    data = {}
    tempData = {}
    for i in dataDump:
        tempData["name"] = i[1]
        tempData["barcode"] = i[0]
        tempData["price"] = i[2]
        tempData["stock"] = i[3]

        data[i[0]] = tempData
        tempData = {}

    return data


def generate_barcode():
    pass
    # This is the new problem!


app = Flask(__name__)
api = Api(app)

product_put_args = reqparse.RequestParser()
product_put_args.add_argument("barcode", type=int, help="Missing Barcode", required=True)
product_put_args.add_argument("name", type=str, help="Missing Name", required=True)
product_put_args.add_argument("price", type=float, help="Missing Price", required=True)

class Home(Resource):
    def get(self):
        return "Welcome to the shopping system Api"

api.add_resource(Home, "/")


class Product(Resource):
    def get(self, barcode):
        return search_database(barcode=barcode)

api.add_resource(Product, "/product/<int:barcode>")

class Product_add(Resource):
    def post(self):
        args = product_put_args.parse_args()
        product = Product(args['barcode'], args['name'], args['price'], args['quantity'])
        product.add_to_database()
        
api.add_resource(Product_add, "/product/add")


class Product_Stock(Resource):
    def get(self,  barcode):
        return check_stock(barcode)


api.add_resource(Product_Stock, "/product/stock/<int:barcode>")


class Product_all(Resource):
    def get(self):
        return product_get_all()


api.add_resource(Product_all, "/product/all")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080,debug=True)  # For Replit
    #app.run(debug=True)  # For Pycharm