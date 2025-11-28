from parsers.MetroParser import MetroParser
from database import get_db,insert_product, select_product_by_name, Product
# from parsers.MetroParser import parser

if __name__ == "__main__":
    url1 = "https://online.metro-cc.ru/category/siry"
    url2 = "https://online.metro-cc.ru/category/myasnye/myaso"
    url3 = "https://online.metro-cc.ru/category/detskie-tovary"
    url4 = "https://online.metro-cc.ru/category/avtotovary"
    parser = MetroParser(url3)
    res = parser.parse(3)
    try:
        db = next(get_db())
        print(len(res))
        for p in res:
            insert_product(db, p)
            print(select_product_by_name(db,p.name))

    except Exception as e:
        print(f"\n Ошибка: {e}")
        db.rollback()
    finally:
        db.close()
