import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.mashina.kg/search/all/'

result = []
for page in range(1, 6):
    params = {
        "page": page,
        "sort": "id_desc"
    }
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')
    container = soup.find("div", class_="table-view-list")
    models = container.find_all("div", class_="list-item")
    for model in models:
        name = model.find("h2", class_='name').contents[0].strip()
        try:
            img = model.find("img", class_="lazy-image").get("data-src")
        except:
            img = "No image!"
        price_div = model.find("div", class_="block price")
        price = price_div.find("p").find("strong").text

        ls = ["year-miles", "body-type", "volume"]
        desc = ", ".join(model.find("p", class_=x).text.strip() for x in ls)
        print(desc)
        data = {
            "name":name, 
            "desc":desc,
            "price":price,
            "img":img,
        }
        result.append(data)

with open('models.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['name', 'desc', 'price', 'img']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(result)

# Код выводит только ограниченное кол-во машин (штук сто один), но можно вывести все модели. Просто для того чтобы не парсить долго, я ввёл ограничение :)