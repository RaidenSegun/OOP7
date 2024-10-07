import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    # Метод для открытия соединения с базой данных
    def open_connection(self):
        self.connection = sqlite3.connect(self.db_name)  # Открываем соединение с базой данных
        print("Соединение с базой данных установлено.")

    # Метод для закрытия соединения с базой данных
    def close_connection(self):
        if self.connection:
            self.connection.close()  # Закрываем соединение
            print("Соединение с базой данных закрыто.")

    # Упрощенный метод для выполнения SQL-запроса
    def execute_query(self, query):
        cursor = self.connection.cursor()  # Создаем курсор
        cursor.execute(query)  # Выполняем запрос
        self.connection.commit()  # Сохраняем изменения
        return cursor  # Возвращаем курсор

    # Упрощенный метод для поиска пользователя по имени
    def find_user_by_name(self, name):
        search_query = f"SELECT * FROM users WHERE name = '{name}';"  # Формируем строку запроса
        cursor = self.execute_query(search_query)  # Выполняем запрос
        return cursor.fetchall() if cursor else None  # Возвращаем результат

    # Упрощенный метод для выполнения транзакции
    def execute_transaction(self):
        cursor = self.connection.cursor()  # Создаем курсор
        
        # Выполняем несколько запросов в одной транзакции
        cursor.execute("INSERT INTO users (name, role) VALUES ('Яхье', 'customer');")
        cursor.execute("INSERT INTO users (name, role) VALUES ('Бекболот', 'admin');")
        
        self.connection.commit()  # Сохраняем изменения
        print("Транзакция успешно выполнена!")

# Пример использования:
if __name__ == "__main__":
    # Создаем экземпляр менеджера базы данных
    db_manager = DatabaseManager("example.db")

    # Открываем соединение с базой данных
    db_manager.open_connection()

    # Создаем таблицу пользователей (если еще не создана)
    db_manager.execute_query("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT NOT NULL
    );
    """)

    # Выполняем транзакцию, добавляя двух пользователей
    db_manager.execute_transaction()

    # Ищем пользователя по имени
    users = db_manager.find_user_by_name("Яхье")
    print("Найденные пользователи:", users)

    # Закрываем соединение с базой данных
    db_manager.close_connection()