from math import ceil
from random import randint
from flask import Flask
from flask_restful import Api, Resource, reqparse
import sqlite3
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

def searchDatabase(barcode):
    if checkBarcode(barcode):
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(Products).filter_by(barcode=barcode).first()
        if query == None:
            return False
        data = {"barcode": query.barcode, "name": query.name, "price": query.price}
        session.close()
        return data
    return False

def generateBarcode():
    barcode = ""
    for i in range(7):
        barcode = barcode + str(randint(0,9))
    lst = []
    checkNum = [3,1,3,1,3,1,3]
    total = 0 
    for i in barcode:
        lst.append(i)

    for i in range(7):
        total = total + int(lst[i]) * checkNum[i]
        
    roundedTotal = ceil(int(total) / 10.0) * 10
    checkDigit = roundedTotal - total

    barcode = int(barcode + str(checkDigit))

    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Products).filter_by(barcode=barcode).first()
    if query == None:
        return barcode
    else:
        generateBarcode()

def checkBarcode(barcode):
    checkDigit = str(barcode)[-1]
    lst = []
    checkNum = [3,1,3,1,3,1,3]
    total = 0 
    for i in str(barcode):
        lst.append(i)

    for i in range(7):
        total = total + int(lst[i]) * checkNum[i]
        
    roundedTotal = ceil(int(total) / 10.0) * 10
    total = roundedTotal - total
    
    if int(total) == int(checkDigit):
        return True
    else:
        return False


class Product:
    def __init__(self, barcode, name, price, quantity):
        self.barcode = barcode
        self.name = name
        self.price = price
        self.quantity = quantity

    def addToDatabase(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(Products).filter_by(barcode=self.barcode).first()

        if query is None:
            if checkBarcode(self.barcode):
                product = Products(barcode=self.barcode, name=self.name, price=self.price, quantity=self.quantity)
                session.add(product)
                session.commit()
                session.close()
                return True
        session.close()
        return False

def deleteProducts(barcode):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(Products).filter_by(barcode=barcode).first()
        if query is None:
            return False
        session.delete(query)
        session.commit()
    except UnmappedInstanceError:
        session.commit()
        session.close()
        return False
    session.close()
    return True

def renameBarcode(barcode, new_barcode):
    if checkBarcode(new_barcode):
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(Products).filter_by(barcode=barcode).first()
        if query is None:
            return False
        query.barcode = new_barcode
        session.commit()
        session.close()
        return True
    return False

def renameProduct(barcode, new_name):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Products).filter_by(barcode=barcode).first()
    if query is None:
        return False
    query.name = new_name
    session.commit()
    session.close()

def newPrice(barcode, new_price):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Products).filter_by(barcode=barcode).first()
    if query is None:
        return False
    query.price = new_price
    session.commit()
    session.close()

def checkStock(barcode):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Products).filter_by(barcode=barcode).first()
    session.close()
    if query is None:
        return False
    data = {"quantity": query.quantity}
    return data

def setStock(barcode, amount):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(Products).filter_by(barcode=barcode).first()
        if query is None:
            return False
        query.quantity = amount
        session.commit()
        session.close()
    except:
        return False
    else:
        return True

def increaseStock(barcode, increase_amount):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(Products).filter_by(barcode=barcode).first()
        if query is None:
            return False
        query.quantity = query.quantity + increase_amount
        session.commit()
        session.close()
    except:
        return False
    else:
        return True

def decreaseStock(barcode, decreasing_amount):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(Products).filter_by(barcode=barcode).first()
        if query == None:
            return False
        query.quantity = query.quantity - decreasing_amount
        if query.quantity < 0:
            query.quantity = 0
        session.commit()
        session.close()
    except:
        return False
    else:
        return True

def productGetAll():
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



# for i in range(10):
#    
# p1 = Product(5901234123457, "Milk", 4.00, 3)

# print(search_database(5901234123457))

# print(p1.decrease_stock(17))

# print(p1.increase_stock(17))

app = Flask(__name__)
api = Api(app)


class home(Resource):
    def get(self):
        return "Welcome to the shopping system Api"


api.add_resource(home, "/")


class productSearch(Resource):
    def get(self, barcode):
        return searchDatabase(barcode=barcode)


api.add_resource(productSearch, "/product/<int:barcode>")

product_post_args = reqparse.RequestParser()
product_post_args.add_argument("barcode", type=str, help="Missing Barcode", required=True)
product_post_args.add_argument("name", type=str, help="Missing Name", required=True)
product_post_args.add_argument("price", type=float, help="Missing Price", required=True)
product_post_args.add_argument("quantity", type=int, help="Missing Quantity", required=True)


class productAdd(Resource):
    def post(self):
        args = product_post_args.parse_args()

        if args['barcode'] == "gen":
            barcode = int(generateBarcode())
        else:
            barcode = int(args['barcode'])
        name = args['name']
        price = args['price']
        quantity = args['quantity']

        product = Product(barcode, name, price, quantity)
        product.addToDatabase()


api.add_resource(productAdd, "/product/add")

product_stock_put_args = reqparse.RequestParser()
product_stock_put_args.add_argument("quantity", type=int, help="Missing quantity", required=True)
product_stock_put_args.add_argument("operation", type=str, help="Missing operation", required=True)


class productStock(Resource):
    def get(self, barcode):
        return checkStock(barcode)

    def put(self, barcode):
        args = product_stock_put_args.parse_args()
        if args['operation'] == "set":
            setStock(barcode, args['quantity'])
        if args['operation'] == "increase":
            increaseStock(barcode, args['quantity'])
        if args['operation'] == "decrease":
            decreaseStock(barcode, args['quantity'])
        return searchDatabase(barcode)


api.add_resource(productStock, "/product/stock/<int:barcode>")

class productDelete(Resource):
    def delete(self, barcode):
        productDelete(barcode)

api.add_resource(productDelete, "/product/delete/<int:barcode>")


class productAll(Resource):
    def get(self):
        return productGetAll()


api.add_resource(productAll, "/product/all")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080,debug=True)  # For Replit
    #app.run(debug=True)  # For Pycharm
