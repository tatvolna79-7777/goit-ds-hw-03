"""
Завдання 1: розробити Python скрипт, який використовує бібліотеку PyMongo 
для реалізації основних CRUD (Create, Read, Update, Delete) операцій у MongoDB.
CRUD-скрипт для роботи з колекцією cats у базі даних MongoDB.

Create (insert) — зроблено вручну через MongoDB Compass.

База даних: hw_3
Колекція: cats

Документ має структуру:
{
    "_id": ObjectId,
    "name": str,
    "age": int,
    "features": list[str]
}
"""

from pymongo import MongoClient
from pymongo.errors import PyMongoError

MONGO_URI = (
    "mongodb+srv://tatvolna79_db_user:vn8dEGYChRSnwiH9@mongo-main.bfws29n.mongodb.net/"
    "?retryWrites=true&w=majority"
)


DB_NAME = "hw_3"
COLLECTION_NAME = "cats"


def get_collection():
    """
    Підключається до MongoDB та повертає колекцію cats.

    Returns:
        Collection: об'єкт колекції MongoDB

    Raises:
        PyMongoError: якщо виникла помилка підключення
    """
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        return db[COLLECTION_NAME]
    except PyMongoError as error:
        raise PyMongoError(f"Помилка підключення до MongoDB: {error}") from error


#  READ

def get_all_cats():
    """
    Виводить усіх котів із колекції.
    """
    try:
        collection = get_collection()
        for cat in collection.find():
            print(cat)
    except PyMongoError as error:
        print(f"Помилка при читанні всіх котів: {error}")


def get_cat_by_name(name: str):
    """
    Шукає кота за ім'ям та виводить його дані.

    Args:
        name (str): ім'я кота
    """
    try:
        collection = get_collection()
        cat = collection.find_one({"name": name})

        if cat:
            print(cat)
        else:
            print(f"Кота з ім'ям '{name}' не знайдено")
    except PyMongoError as error:
        print(f"Помилка при пошуку кота: {error}")


#  UPDATE

def update_cat_age(name: str, age: int):
    """
    Оновлює вік кота за ім'ям.

    Args:
        name (str): ім'я кота
        age (int): новий вік
    """
    try:
        collection = get_collection()
        result = collection.update_one(
            {"name": name},
            {"$set": {"age": age}},
        )

        if result.matched_count:
            print(f"Вік кота '{name}' оновлено до {age}")
        else:
            print(f"Кота з ім'ям '{name}' не знайдено")
    except PyMongoError as error:
        print(f"Помилка при оновленні віку: {error}")


def add_cat_feature(name: str, feature: str):
    """
    Додає нову характеристику до списку features кота.

    Args:
        name (str): ім'я кота
        feature (str): характеристика
    """
    try:
        collection = get_collection()
        result = collection.update_one(
            {"name": name},
            {"$push": {"features": feature}},
        )

        if result.matched_count:
            print(f"Характеристику додано коту '{name}'")
        else:
            print(f"Кота з ім'ям '{name}' не знайдено")
    except PyMongoError as error:
        print(f"Помилка при додаванні характеристики: {error}")


#  DELETE

def delete_cat_by_name(name: str):
    """
    Видаляє кота з колекції за ім'ям.

    Args:
        name (str): ім'я кота
    """
    try:
        collection = get_collection()
        result = collection.delete_one({"name": name})

        if result.deleted_count:
            print(f"Кота '{name}' видалено")
        else:
            print(f"Кота з ім'ям '{name}' не знайдено")
    except PyMongoError as error:
        print(f"Помилка при видаленні кота: {error}")


def delete_all_cats():
    """
    Видаляє всі записи з колекції cats.

    ⚠️ Увага: дія незворотна.
    """
    try:
        collection = get_collection()
        result = collection.delete_many({})
        print(f"Видалено котів: {result.deleted_count}")
    except PyMongoError as error:
        print(f"Помилка при видаленні всіх котів: {error}")


# ПРИКЛАД ЗАПУСКУ

if __name__ == "__main__":
    print("Усі коти:")
    get_all_cats()

    print("\nПошук кота 'barsik':")
    get_cat_by_name("barsik")

    print("\nОновлення віку кота 'nora':")
    update_cat_age("nora", 12)

    print("\nДодавання характеристики коту 'borik':")
    add_cat_feature("borik", "любить спати")

    print("\nВидалення кота 'sima':")
    delete_cat_by_name("sima")

    # ⚠️ Розкоментувати тільки за потреби
    # delete_all_cats()
