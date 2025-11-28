import math
import re
import requests
from bs4 import BeautifulSoup
from database.models import Product
from  decouple import config
class MetroParser:
    __HEADERS = {
        "User-Agent": config("METRO_USER_AGENT"),
        "Accept": config("METRO_ACCEPT"),
        "Accept-Language":config("METRO_ACCEPT_LANGUAGE"),
    }

    def __init__(self,url:str):
        self.__base_url = url

    def parse(self,pages:int = None):
        list_of_products = []
        total_pages = self.__calculate_total_pages()
        # print(total_pages)
        page = 1

        if pages and 0<pages<total_pages:
            total_pages =pages
        while page<=total_pages:
            list_of_products.extend(self.__parse_single_page(page))
            page+=1
        return list_of_products

    def __parse_single_page(self,page_num:int):
        list_of_products = []
        request = requests.get(f"{self.__base_url}?page={page_num}",
        headers=self.__HEADERS,timeout=10)
        soup = BeautifulSoup(request.text, 'lxml')
        products = soup.find_all("div", class_="product-card")

        for product in products:
            product_name = product.find("span", class_="product-card-name__text").get_text(strip=True)
            price_element = product.find("span", class_="product-price")
            href = product.find("a", class_="product-card-photo__link").get("href")
            link = (f"https://online.metro-cc.ru{href}")

            if price_element:
                price_text = price_element.get_text(strip=True)
                price, unit = self.__clean_price_with_unit(price_text)
                list_of_products.append(Product(name=product_name, price=price, unit=unit, link=link))

        return list_of_products


    def __calculate_total_pages(self):
        request = requests.get(self.__base_url,headers= self.__HEADERS,timeout=10)
        soup = BeautifulSoup(request.text, "lxml")
        total = soup.find('span', class_="heading-products-count subcategory-or-type__heading-count")
        print(total)
        if total:
            total = int(total.get_text(strip=True).split()[0]) # результат будет строка "N товара". Поэтому делим её и берём 1-й элемент, то есть число
            return math.ceil(total / 30)
        else:
            return 1 #Если не нашлось, то ищем на 1 странице


    @staticmethod
    def __clean_price_with_unit(price_text):
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


#
# def parser(url: str):
#     list_of_products = []
#     request = requests.get(url, timeout=10)
#     soup = BeautifulSoup(request.text,'lxml')
#
#     elements = int(soup.find("span",class_="heading-products-count").
#                    get_text(strip=True).split()[0])#всего элементов в категории
#     pages = elements//30 if elements%30==0 else elements//30 +1 # на странице всего 30 элементов, чтобы узнать кол-во страниц поделим все элементы на 30
#     page = 1
#     while page <= pages:
#         print(page)
#         request = requests.get(f"{url}?page={page}")
#         soup = BeautifulSoup(request.text, 'lxml')
#         products = soup.find_all("div", class_="product-card")
#
#         for product in products:
#             product_name =  product.find("span", class_="product-card-name__text").get_text(strip=True)
#             price_element = product.find("span", class_="product-price")
#             href = product.find("a", class_="product-card-photo__link").get("href")
#             link = (f"https://online.metro-cc.ru{href}")
#
#
#             if price_element:
#                 price_text = price_element.get_text(strip=True)
#                 price, unit = clean_price_with_unit(price_text)
#                 list_of_products.append(Product(name = product_name,price = price, unit= unit,link=link))
#         page+=1
#     return list_of_products
#
# def clean_price_with_unit(price_text):
#     """
#     Возвращает цену и единицу измерения
#     """
#     match = re.match(r'([\d\s\xa0]+)д\/([а-я]+)', price_text)
#     if match:
#         price_part = match.group(1)
#         unit = match.group(2)
#         # Очищаем цену
#         price = int(price_part.replace('\xa0', '').replace(' ', ''))
#         return price, unit
#     return 0, ''