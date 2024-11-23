"""
Модуль для виконання SQL-запитів до бази даних PostgreSQL 
та збереження результатів у CSV файли.
"""


import csv
from pathlib import Path
from connect import create_connection
from typing import List, Dict, Any, Optional



def execute_query(connection, query: str) -> Optional[List[Dict[str, Any]]]:
    """
    Виконує SQL-запит та повертає результат.
    
    Args:
        connection: З'єднання з базою даних
        query (str): SQL-запит для виконання
        
    Returns:
        Optional[List[Dict[str, Any]]]: Результат запиту або None у разі помилки
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            return [dict(zip(columns, row)) for row in results]

    except Exception as e:
        print(f"Помилка виконання запиту: {e}")
        return None


def save_to_csv(results: List[Dict[str, Any]], filename: str) -> None:
    """
    Зберігає результати запиту у CSV файл.
    
    Args:
        results: Результати запиту
        filename: Назва файлу для збереження
    """
    if not results:
        return

    # Створюємо директорію для результатів якщо її немає
    output_dir = Path('query_results')
    output_dir.mkdir(exist_ok=True)
    filepath = output_dir / f"{filename}.csv"

    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"Результати збережено у файл: {filepath}")
    except Exception as e:
        print(f"Помилка збереження файлу: {e}")


def main():
    """
    Головна функція для виконання запитів та збереження результатів.
    """
    queries = {
        "user_tasks": """
            SELECT u.fullname, t.id, t.title, t.description, s.name as status
            FROM tasks t
            JOIN status s ON t.status_id = s.id
            JOIN users u ON t.user_id = u.id
            WHERE t.user_id = 50
        """,

        "tasks_by_status": """
            SELECT s.name as status, t.title, t.description, u.fullname
            FROM tasks t
            JOIN users u ON t.user_id = u.id
            JOIN status s ON t.status_id = s.id
            WHERE t.status_id = (SELECT id FROM status WHERE name = 'Нове')
        """,

        "users_without_tasks": """
            SELECT *
            FROM users
            WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)
        """,

        "uncompleted_tasks": """
            SELECT t.id, t.title, t.description, s.name as status, u.fullname
            FROM tasks t
            JOIN status s ON t.status_id = s.id
            JOIN users u ON t.user_id = u.id
            WHERE s.name != 'Завершене'
        """,

        "users_by_email": """
            SELECT *
            FROM users
            WHERE email LIKE '%@example.org'
        """,

        "task_statistics": """
            SELECT s.name, COUNT(t.id) as tasks_count
            FROM status s
            LEFT JOIN tasks t ON s.id = t.status_id
            GROUP BY s.name
            ORDER BY tasks_count DESC
        """,

        "tasks_by_user_email_domain": """
            SELECT t.id, t.title, t.description, u.fullname, u.email
            FROM tasks t
            JOIN users u ON t.user_id = u.id
            WHERE u.email LIKE '%@example.com';
        """,

        "tasks_without_description": """
            SELECT t.id, t.title, t.description, u.fullname
            FROM tasks t
            JOIN users u ON t.user_id = u.id
            WHERE t.description IS NULL OR trim(t.description) = '';
        """,

        "in_progress_status_tasks": """
            SELECT u.fullname, t.title, t.description
            FROM users u
            JOIN tasks t ON u.id = t.user_id
            JOIN status s ON t.status_id = s.id
            WHERE s.name = 'Виконується';
        """,

        "users_and_tasks_statistics": """
            SELECT 
                u.id,
                u.fullname,
                u.email,
                COUNT(t.id) as tasks_count
            FROM users u
            LEFT JOIN tasks t ON u.id = t.user_id
            GROUP BY u.id, u.fullname, u.email
            ORDER BY tasks_count DESC
        """
    }

    try:
        with create_connection() as conn:
            for filename, query in queries.items():
                print(f"\nВиконання запиту: {filename}")
                results = execute_query(conn, query)
                if results:
                    save_to_csv(results, filename)
                else:
                    print("Запит не повернув результатів")

    except Exception as e:
        print(f"Помилка підключення до бази даних: {e}")


if __name__ == "__main__":
    main()
