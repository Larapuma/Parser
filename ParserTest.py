from itertools import product
import re
import requests
from bs4 import BeautifulSoup
from model import Product



def parser(url: str):
    list_of_products = []
    request = requests.get(url)
    soup = BeautifulSoup(request.text,'lxml')

    elements = int(soup.find("span",class_="heading-products-count").get_text(strip=True).split()[0])#всего элементов в категории
    pages = elements//30 if elements%30==0 else elements//30 +1 # на странице всего 30 элементов, чтобы узнать кол-во страниц поделим все элементы на 30
    page = 1
    while page <= pages:
        print(page)
        request = requests.get(f"{url}?page={page}")
        soup = BeautifulSoup(request.text, 'lxml')
        products = soup.find_all("div", class_="product-card")

        for product in products:
            product_name =  product.find("span", class_="product-card-name__text").get_text(strip=True)
            price_element = product.find("span", class_="product-price")
            href = product.find("a", class_="product-card-photo__link").get("href")
            link = (f"https://online.metro-cc.ru{href}")


            if price_element:
                price_text = price_element.get_text(strip=True)
                price, unit = clean_price_with_unit(price_text)
                list_of_products.append(Product(name = product_name,price = price, unit= unit,link=link))
        page+=1
    return list_of_products

def clean_price_with_unit(price_text):
    """
    Возвращает цену и единицу измерения
    """
    match = re.match(r'([\d\s\xa0]+)д\/([а-я]+)', price_text)
    if match:
        price_part = match.group(1)
        unit = match.group(2)
        # Очищаем цену
        price = int(price_part.replace('\xa0', '').replace(' ', ''))
        return price, unit
    return 0, ''

if __name__ == "__main__":
    url = "https://online.metro-cc.ru/category/siry"#сыры
    url2 = "https://online.metro-cc.ru/category/myasnye/myaso"
    url3 = "https://online.metro-cc.ru/category/molochnye-prodkuty-syry-i-yayca"
    url4 = "https://online.metro-cc.ru/category/vse-dlya-remonta"
    res = parser(url = url4)
    for p in res:
        print(p)
