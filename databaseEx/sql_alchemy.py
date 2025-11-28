from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.testing.suite.test_reflection import users

#Base Session - классы тут
Base = declarative_base()# класс от которого мы наследуемся
engine = create_engine("sqlite:///demo.db") #в скобках указываем бд
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

Base.metadata.create_all(engine)
#
# maria = User(name = "Мария", age = 19)
# alex = User(name = "Алексей", age = 23)
# # session.add(maria)
# # session.add(alex)
# session.add_all([maria,alex])
# session.commit()

users = session.query(User).filter_by(name = "Мария").all()
for user in users:
    print(f"{user.name} {user.age}")


