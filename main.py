from parsers.MetroParser import MetroParser
# from parsers.MetroParser import parser
if __name__ == "__main__":
    url1 = "https://online.metro-cc.ru/category/siry"#сыры
    url2 = "https://online.metro-cc.ru/category/myasnye/myaso"
    url3 = "https://online.metro-cc.ru/category/molochnye-prodkuty-syry-i-yayca"
    url4 = "https://online.metro-cc.ru/category/vse-dlya-remonta"
    parser = MetroParser(url4)
    res = parser.parse(2)
    for p in res:
        print(p)
    print(len(res))
