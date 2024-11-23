"""Модуль для встановлення з'єднання з базою даних PostgreSQL."""


import os
from contextlib import contextmanager
from typing import Generator
import configparser
import psycopg2
from psycopg2.extensions import connection


# Визначаємо шлях до файлу конфігурації
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.ini')


def get_db_config(config_path: str = CONFIG_PATH) -> dict:
    """
    Читає конфігурацію бази даних з файлу.
    
    Args:
        config_path (str): Шлях до файлу конфігурації
        
    Returns:
        dict: Словник з параметрами підключення
        
    Raises:
        FileNotFoundError: Якщо файл конфігурації не знайдено
        configparser.Error: Якщо виникла помилка при читанні конфігурації
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Файл конфігурації не знайдено: {config_path}")

    config = configparser.ConfigParser()
    config.read(config_path)

    if 'PostgreSQL' not in config:
        raise configparser.Error("Секція 'PostgreSQL' відсутня в файлі конфігурації")

    return {
        "host": config.get('PostgreSQL', 'HOST'),
        "database": config.get('PostgreSQL', 'DATABASE'),
        "user": config.get('PostgreSQL', 'USER'),
        "password": config.get('PostgreSQL', 'PASSWORD'),
        "port": config.get('PostgreSQL', 'PORT')
    }

@contextmanager
def create_connection() -> Generator[connection, None, None]:
    """
    Створює з'єднання з базою даних PostgreSQL використовуючи контекстний менеджер.
    
    Yields:
        connection: Об'єкт з'єднання з базою даних PostgreSQL
    
    Raises:
        psycopg2.Error: Якщо виникла помилка при з'єднанні з базою даних
        FileNotFoundError: Якщо файл конфігурації не знайдено
    """
    conn = None
    try:
        # Отримання параметрів підключення з конфігураційного файлу
        db_config = get_db_config()

        # Встановлення з'єднання з базою даних
        conn = psycopg2.connect(**db_config)
        yield conn
    except psycopg2.Error as e:
        print(f"Помилка з'єднання з PostgreSQL: {e}")
        raise
    except FileNotFoundError:
        print("Помилка: Файл конфігурації не знайдено")
        raise
    except configparser.Error as e:
        print(f"Помилка читання конфігурації: {e}")
        raise
    finally:
        if conn is not None:
            conn.rollback()  # Відкат незавершених транзакцій
            conn.close()     # Закриття з'єднання


if __name__ == "__main__":
    # Тестування з'єднання
    try:
        with create_connection() as conn:
            print("Успішне підключення до бази даних")
    except Exception as e:
        print(f"Помилка: {e}")
