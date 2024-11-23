"""
Модуль для створення таблиць в базі даних PostgreSQL.
Створює таблиці users, status та tasks з відповідними зв'язками.
"""


from connect import create_connection
import psycopg2


def create_table(connection, query: str) -> None:
    """
    Створює таблицю в базі даних за допомогою наданого SQL-запиту.
    
    Args:
        connection: З'єднання з базою даних
        query (str): SQL-запит для створення таблиці
        
    Raises:
        psycopg2.Error: Якщо виникла помилка при створенні таблиці
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()  # Збереження змін
    except psycopg2.Error as e:
        print(f"Помилка створення таблиці: {e}")
        raise


if __name__ == '__main__':
    # SQL-запит для створення таблиці користувачів
    SQL_CREATE_USERS_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,            -- Унікальний ідентифікатор користувача
        fullname VARCHAR(100) NOT NULL,   -- Повне ім'я користувача
        email VARCHAR(100) UNIQUE NOT NULL -- Унікальна електронна адреса
    );
    """

    # SQL-запит для створення таблиці статусів
    SQL_CREATE_STATUS_TABLE = """
    CREATE TABLE IF NOT EXISTS status (
        id SERIAL PRIMARY KEY,          -- Унікальний ідентифікатор статусу
        name VARCHAR(50) UNIQUE NOT NULL -- Унікальна назва статусу
    );
    """

    # SQL-запит для створення таблиці завдань
    SQL_CREATE_TASKS_TABLE = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,           -- Унікальний ідентифікатор завдання
        title VARCHAR(100) NOT NULL,     -- Назва завдання
        description TEXT,                -- Опис завдання
        status_id INTEGER NOT NULL,      -- Зовнішній ключ на таблицю status
        user_id INTEGER NOT NULL,        -- Зовнішній ключ на таблицю users
        FOREIGN KEY (status_id) REFERENCES status (id)
            ON DELETE RESTRICT           -- Заборона видалення використовуваного статусу
            ON UPDATE CASCADE,           -- Каскадне оновлення при зміні id статусу
        FOREIGN KEY (user_id) REFERENCES users (id)
            ON DELETE CASCADE            -- Видалення завдань при видаленні користувача
            ON UPDATE CASCADE            -- Каскадне оновлення при зміні id користувача
    );
    """

    try:
        with create_connection() as conn:
            # Створення таблиці users
            create_table(conn, SQL_CREATE_USERS_TABLE)
            print("Таблицю 'users' успішно створено")

            # Створення таблиці status
            create_table(conn, SQL_CREATE_STATUS_TABLE)
            print("Таблицю 'status' успішно створено")

            # Створення таблиці tasks
            create_table(conn, SQL_CREATE_TASKS_TABLE)
            print("Таблицю 'tasks' успішно створено")

    except Exception as e:
        print(f"Помилка: {e}")
