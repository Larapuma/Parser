from sqlalchemy import  Column, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Product(Base):
    """Модель товара."""
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float)
    unit = Column(String)
    link = Column(String,nullable=False)
    def __repr__(self):
        return f"Product(name = {self.name}, price = {self.price})."

