"""
Скрипт для імпорту даних з JSON файлів у MongoDB.

Підключається до кластера MongoDB Atlas, створює (або очищує)
колекції 'quotes' та 'authors' у базі даних 'quotes_db',
та імпортує відповідні дані з файлів quotes.json та authors.json.

Файли JSON знаходяться у тій же папці, що і скрипт.
"""
import json
from pymongo import MongoClient


# Підключення до кластера MongoDB Atlas
client = MongoClient(
   "mongodb+srv://tatvolna79_db_user:vn8dEGYChRSnwiH9@mongo-main.bfws29n.mongodb.net/"
   "?retryWrites=true&w=majority"
)

# Вказуємо базу даних
db = client.quotes_db

# Створюємо або отримуємо колекції
quotes_collection = db.quotes
authors_collection = db.authors

# Очищуємо колекції, якщо вони вже існують
quotes_collection.delete_many({})
authors_collection.delete_many({})

# Імпортуємо дані з файлу quotes.json
with open("quotes.json", "r", encoding="utf-8") as f:
    quotes_data = json.load(f)
    quotes_collection.insert_many(quotes_data)

# Імпортуємо дані з файлу authors.json
with open("authors.json", "r", encoding="utf-8") as f:
    authors_data = json.load(f)
    authors_collection.insert_many(authors_data)

print("Дані успішно імпортовано в MongoDB!")
