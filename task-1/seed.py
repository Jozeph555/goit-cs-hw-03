"""
Модуль для заповнення таблиць випадковими даними.
"""


from faker import Faker
import psycopg2
from connect import create_connection


fake = Faker('uk_UA')  # Використовуємо українську локалізацію


def insert_users(connection, num_users: int = 10) -> None:
    """
    Додає випадкових користувачів до таблиці users.
    
    Args:
        connection: З'єднання з базою даних
        num_users (int): Кількість користувачів для створення
    """
    cursor = connection.cursor()
    for _ in range(num_users):
        cursor.execute(
            """
            INSERT INTO users (fullname, email)
            VALUES (%s, %s)
            RETURNING id;
            """,
            (fake.name(), fake.email())
        )
    connection.commit()
    print(f"Додано {num_users} користувачів")

def insert_statuses(connection) -> None:
    """
    Додає статуси до таблиці status.
    
    Args:
        connection: З'єднання з базою даних
    """
    statuses = ['Нове', 'Виконується', 'Завершене']
    cursor = connection.cursor()

    for status in statuses:
        cursor.execute(
            """
            INSERT INTO status (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING;
            """,
            (status,)
        )
    connection.commit()
    print("Статуси додано")

def insert_tasks(connection, num_tasks: int = 20) -> None:
    """
    Додає випадкові завдання до таблиці tasks.
    
    Args:
        connection: З'єднання з базою даних
        num_tasks (int): Кількість завдань для створення
    """
    # Отримуємо існуючі ID користувачів та статусів
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM status")
    status_ids = [row[0] for row in cursor.fetchall()]

    # Додаємо завдання
    for _ in range(num_tasks):
        cursor.execute(
            """
            INSERT INTO tasks (title, description, status_id, user_id)
            VALUES (%s, %s, %s, %s)
            """,
            (
                fake.sentence(nb_words=3),  # Коротка назва завдання
                fake.text(max_nb_chars=200),  # Опис завдання
                fake.random_element(status_ids),  # Випадковий статус
                fake.random_element(user_ids)  # Випадковий користувач
            )
        )
    connection.commit()
    print(f"Додано {num_tasks} завдань")

def main():
    """
    Головна функція для заповнення всіх таблиць.
    """
    # Встановлюємо кількість випадкових користувачів
    users = 100
    # Встановлюємо кількість випадкових завдань
    tasks = 300

    try:
        with create_connection() as connection:
            # Додаємо користувачів
            insert_users(connection, users)

            # Додаємо статуси
            insert_statuses(connection)

            # Додаємо завдання
            insert_tasks(connection, tasks)

            print("Всі дані успішно додано")

    except psycopg2.Error as e:
        print(f"Помилка бази даних: {e}")
    except Exception as e:
        print(f"Помилка: {e}")


if __name__ == "__main__":
    main()
