"""
Модуль для підключення до MongoDB Atlas.
"""


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import configparser
from typing import Optional
import certifi


def get_database_connection() -> Optional[MongoClient]:
    """
    Створює підключення до MongoDB Atlas використовуючи конфігураційний файл.
    
    Returns:
        Optional[MongoClient]: Об'єкт підключення до бази даних або None у разі помилки
        
    Raises:
        ConfigError: Якщо виникла помилка при читанні конфігурації
        ConnectionError: Якщо виникла помилка при підключенні до бази даних
    """
    try:
        # Читаємо конфігурацію
        config = configparser.ConfigParser()
        config.read('config.ini')
        uri = config['MongoDB']['CONNECTION_STRING']

        # Створюємо клієнт з використанням ServerApi версії 1 та SSL сертифікатом
        client = MongoClient(
            uri,
            server_api=ServerApi('1'),
            tlsCAFile=certifi.where(),
            tls=True,
            tlsAllowInvalidCertificates=True
        )
        return client

    except Exception as e:
        print(f"Помилка підключення до MongoDB: {e}")
        return None


def test_connection() -> None:
    """
    Тестує підключення до бази даних шляхом виконання ping-команди.
    """
    try:
        client = get_database_connection()
        if client:
            # Перевіряємо підключення
            client.admin.command('ping')
            print("Успішне підключення до MongoDB!")

            # Додаткова інформація про бази даних
            print("\nДоступні бази даних:")
            for db_name in client.list_database_names():
                print(f"- {db_name}")

    except Exception as e:
        print(f"Помилка при тестуванні підключення: {e}")


if __name__ == "__main__":
    test_connection()
