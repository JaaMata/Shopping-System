from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name, self.fullname, self.nickname)

Base.metadata.create_all(engine)

ed_user = User(name="ed",fullname="Ed Jones", nickname="edsnickname")
print(ed_user.name)

Session = sessionmaker(bind=engine)
session = Session()

session.add(ed_user)

our_user = session.query(User).filter_by(name='ed').first()

print(ed_user is our_user)