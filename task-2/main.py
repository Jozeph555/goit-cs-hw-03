"""
Модуль для роботи з MongoDB, який реалізує CRUD операції.
База даних містить інформацію про котів: їх імена, вік та характеристики.
"""


from typing import Optional, Dict, Any
from connect import get_database_connection


def show_all_cats() -> None:
    """Виведення всіх записів з колекції."""
    try:
        client = get_database_connection()
        if client:
            db = client["cats_db"]
            collection = db["cats"]
            cats = collection.find()

            print("\nСписок всіх котів:")
            for cat in cats:
                print_cat_info(cat)
    except Exception as e:
        print(f"Помилка при отриманні даних: {e}")


def find_cat_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Пошук кота за ім'ям.
    
    Args:
        name (str): Ім'я кота
        
    Returns:
        Optional[Dict[str, Any]]: Інформація про кота або None, якщо кіт не знайдений
    """
    try:
        client = get_database_connection()
        if client:
            db = client["cats_db"]
            collection = db["cats"]
            cat = collection.find_one({"name": name})

            if cat:
                print("\nЗнайдено кота:")
                print_cat_info(cat)
                return cat
            else:
                print(f"\nКота з ім'ям {name} не знайдено")
                return None
    except Exception as e:
        print(f"Помилка при пошуку: {e}")
        return None


def update_cat_age(name: str, new_age: int) -> None:
    """
    Оновлення віку кота за ім'ям.
    
    Args:
        name (str): Ім'я кота
        new_age (int): Новий вік
    """
    try:
        client = get_database_connection()
        if client:
            db = client["cats_db"]
            collection = db["cats"]
            result = collection.update_one(
                {"name": name},
                {"$set": {"age": new_age}}
            )

            if result.modified_count:
                print(f"\nВік кота {name} оновлено на {new_age}")
            else:
                print(f"\nКота з ім'ям {name} не знайдено")
    except Exception as e:
        print(f"Помилка при оновленні: {e}")


def add_cat_feature(name: str, new_feature: str) -> None:
    """
    Додавання нової характеристики коту за ім'ям.
    
    Args:
        name (str): Ім'я кота
        new_feature (str): Нова характеристика
    """
    try:
        client = get_database_connection()
        if client:
            db = client["cats_db"]
            collection = db["cats"]
            result = collection.update_one(
                {"name": name},
                {"$addToSet": {"features": new_feature}}
            )

            if result.modified_count:
                print(f"\nДодано нову характеристику для кота {name}")
            else:
                print(f"\nКота з ім'ям {name} не знайдено")
    except Exception as e:
        print(f"Помилка при додаванні характеристики: {e}")


def delete_cat_by_name(name: str) -> None:
    """
    Видалення кота за ім'ям.
    
    Args:
        name (str): Ім'я кота
    """
    try:
        client = get_database_connection()
        if client:
            db = client["cats_db"]
            collection = db["cats"]
            result = collection.delete_one({"name": name})

            if result.deleted_count:
                print(f"\nКота {name} видалено")
            else:
                print(f"\nКота з ім'ям {name} не знайдено")
    except Exception as e:
        print(f"Помилка при видаленні: {e}")


def delete_all_cats() -> None:
    """Видалення всіх записів з колекції."""
    try:
        client = get_database_connection()
        if client:
            db = client["cats_db"]
            collection = db["cats"]
            result = collection.delete_many({})
            print(f"\nВидалено {result.deleted_count} записів")
    except Exception as e:
        print(f"Помилка при видаленні всіх записів: {e}")


def print_cat_info(cat: Dict[str, Any]) -> None:
    """
    Виведення інформації про кота.
    
    Args:
        cat (Dict[str, Any]): Словник з інформацією про кота
    """
    print(f"\nІм'я: {cat['name']}")
    print(f"Вік: {cat['age']}")
    print("Характеристики:", ", ".join(cat['features']))


def main():
    """Головна функція для демонстрації роботи з базою даних."""
    while True:
        print("\nОберіть операцію:")
        print("1. Показати всіх котів")
        print("2. Знайти кота за ім'ям")
        print("3. Оновити вік кота")
        print("4. Додати характеристику коту")
        print("5. Видалити кота")
        print("6. Видалити всіх котів")
        print("0. Вийти")

        choice = input("\nВаш вибір: ")

        if choice == "1":
            show_all_cats()
        elif choice == "2":
            name = input("Введіть ім'я кота: ")
            find_cat_by_name(name)
        elif choice == "3":
            name = input("Введіть ім'я кота: ")
            try:
                age = int(input("Введіть новий вік: "))
                update_cat_age(name, age)
            except ValueError:
                print("Помилка: вік повинен бути числом")
        elif choice == "4":
            name = input("Введіть ім'я кота: ")
            feature = input("Введіть нову характеристику: ")
            add_cat_feature(name, feature)
        elif choice == "5":
            name = input("Введіть ім'я кота: ")
            delete_cat_by_name(name)
        elif choice == "6":
            confirm = input("Ви впевнені? (y/n): ")
            if confirm.lower() == 'y':
                delete_all_cats()
        elif choice == "0":
            print("\nДо побачення!")
            break
        else:
            print("\nНеправильний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
