from database.models import Base
from database.session import engine

def init_db():
    """
    Создаёт все таблицы в БД, если их ещё нет.
    """
    Base.metadata.create_all(bind=engine)

def drop_db():
    """
    Удаляет все таблицы из БД.
    """
    Base.metadata.drop_all(bind=engine)

def reset_db():
    """
    Пересоздаёт БД с нуля: удаляет старые таблицы и создаёт новые.
    """
    drop_db()
    init_db()



