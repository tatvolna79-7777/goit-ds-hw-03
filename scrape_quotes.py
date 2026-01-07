"""
Завдання 2: виконати скрапінг сайту http://quotes.toscrape.com. 
Отримати два файли: quotes.json — інформація про цитати з усіх сторінок сайту,
та authors.json — інформація про авторів зазначених цитат.
"""

import json
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://quotes.toscrape.com"

# Змінні для збереження всіх цитат та авторів
all_quotes = []
all_authors = {}

page = 1  # pylint: disable=C0103

"""
Скрапінг всіх цитат та авторів з сайту quotes.toscrape.com.

Цикл проходить по всіх сторінках сайту, збираючи:
- текст цитати,
- ім'я автора,
- теги цитати.

Якщо автор ще не доданий у словник all_authors,
збирається додаткова інформація про автора:
- повне ім'я,
- дата народження,
- місце народження,
- короткий опис.

Результат зберігається у JSON файли:
- quotes.json — всі цитати зі всіма тегами,
- authors.json — інформація про авторів.
"""
while True:
    page_url = f"{BASE_URL}/page/{page}/"  # pylint: disable=C0103
    response = requests.get(page_url, timeout=10)
    soup = BeautifulSoup(response.text, "lxml")

    # Знаходимо всі блоки цитат на сторінці
    quotes = soup.find_all("div", class_="quote")
    if not quotes:
        break  # Якщо цитат немає — кінець сторінок

    for quote in quotes:
        # Отримуємо текст цитати
        text = quote.find("span", class_="text").text

        # Отримуємо ім'я автора
        author = quote.find("small", class_="author").text

        # Отримуємо теги цитати у вигляді списку
        tags = [tag.text for tag in quote.find_all("a", class_="tag")]

        # Додаємо цитату у список усіх цитат
        all_quotes.append({"quote": text, "author": author, "tags": tags})

        # Якщо автора ще немає у словнику, збираємо додаткову інформацію
        if author not in all_authors:
            author_url = BASE_URL + quote.find("a")["href"]
            author_resp = requests.get(author_url, timeout=10)
            author_soup = BeautifulSoup(author_resp.text, "lxml")

            # Отримуємо дату народження
            born_date = author_soup.find("span", class_="author-born-date").text

            # Отримуємо місце народження
            born_location = author_soup.find("span", class_="author-born-location").text

            # Отримуємо опис автора
            description = author_soup.find("div", class_="author-description").text.strip()

            # Додаємо автора у словник all_authors
            all_authors[author] = {
                "fullname": author,
                "born_date": born_date,
                "born_location": born_location,
                "description": description,
            }

    page += 1

# Збереження зібраних даних у JSON файли
with open("quotes.json", "w", encoding="utf-8") as f:
    json.dump(all_quotes, f, ensure_ascii=False, indent=4)

with open("authors.json", "w", encoding="utf-8") as f:
    json.dump(list(all_authors.values()), f, ensure_ascii=False, indent=4)
