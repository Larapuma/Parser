urls = [
 "https://online.metro-cc.ru/category/siry",
 "https://online.metro-cc.ru/category/myasnye/myaso",
 "https://online.metro-cc.ru/category/molochnye-prodkuty-syry-i-yayca",
"https://online.metro-cc.ru/category/avtotovary",]
import math
import requests
from bs4 import BeautifulSoup
import time
import logging

logging.basicConfig(level=logging.INFO)


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
}



def foo(url):
    for attempt in range(5):
        try:
            logging.info(f"Попытка {attempt + 1} для {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml")
            total_element = soup.find('span', class_='heading-products-count')

            if total_element:
                text = total_element.get_text(strip=True)
                total = int(text.split()[0])
                return math.ceil(total / 30)
            else:
                logging.warning("Элемент с количеством товаров не найден")

        except requests.RequestException as e:
            logging.error(f"Ошибка запроса: {e}")
            time.sleep(2)  # Пауза перед повторной попыткой

    return 1  # По умолчанию
print(foo(urls[3]))