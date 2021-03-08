import sqlite3

def create_tables():
    db = sqlite3.connect("database.db")
    c = db.cursor()
    
    c.execute("""CREATE TABLE IF NOT EXSIST Products
               (id INTERGER FIELD)""")





if __name__ == "__main__":
    create_tables()
