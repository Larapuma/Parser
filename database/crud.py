from sqlalchemy.orm import Session
from database.models import Product



def insert_product(db:Session, product: Product):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def select_product_by_name(db:Session, name:str)-> list:
    return db.query(Product) \
        .filter(Product.name.ilike(f"%{name}%")) \
        .all()



