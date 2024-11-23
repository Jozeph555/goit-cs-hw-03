"""
Модуль для виконання запитів, що модифікують дані в базі даних PostgreSQL.
Містить функції для оновлення, додавання та видалення даних.
"""


from connect import create_connection
from typing import Optional


def execute_modification_query(connection, query: str, query_name: str) -> None:
    """
    Виконує запит на модифікацію даних.
    
    Args:
        connection: З'єднання з базою даних
        query (str): SQL-запит для виконання
        query_name (str): Назва операції для виводу
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            print(f"Операцію '{query_name}' успішно виконано")
    except Exception as e:
        connection.rollback()
        print(f"Помилка виконання операції '{query_name}': {e}")


def main():
    """
    Головна функція для виконання запитів на модифікацію даних.
    """
    modification_queries = {
        "Оновлення статусу завдання": """
            UPDATE tasks
            SET status_id = (SELECT id FROM status WHERE name = 'Виконується')
            WHERE id = 60;
        """,

        "Додавання нового завдання": """
            INSERT INTO tasks (title, description, status_id, user_id)
            VALUES (
                'Звіт',
                'Надрукувати звіт у трьох примірниках',
                (SELECT id FROM status WHERE name = 'Нове'),
                60
            );
        """,

        "Видалення завдання": """
            DELETE FROM tasks
            WHERE id = 150;
        """,

        "Оновлення імені користувача": """
            UPDATE users
            SET fullname = 'Козаченко Козак'
            WHERE id = 60;
        """
    }

    try:
        with create_connection() as conn:
            # Виконання всіх запитів на модифікацію
            for operation_name, query in modification_queries.items():
                execute_modification_query(conn, query, operation_name)

    except Exception as e:
        print(f"Помилка підключення до бази даних: {e}")


if __name__ == "__main__":
    main()
