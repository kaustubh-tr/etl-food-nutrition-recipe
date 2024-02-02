import psycopg2
from config.config import Config
from db.db_connector import DBConnector

class Food:
    def __init__(self, id, food_name):
        self.id = id
        self.food_name = food_name

    def __str__(self):
        return f"Food(id={self.id}, name={self.food_name})"

    def save_to_db(self):
        try:
            db = DBConnector()
            query = "INSERT INTO food (food_name) VALUES (%s) RETURNING id;"
            db.execute_query(query, (self.food_name,))
            self.id = db.cursor.fetchone()[0]  # Assuming cursor is available in DBConnector
            db.close_connection()
            return self.id
        except Exception as e:
            print("Error:", e)
            return None

    @staticmethod
    def find_by_name(name):
        query = "SELECT id FROM food WHERE LOWER(food_name) = LOWER(%s);"
        try:
            with DBConnector() as db:
                db.execute_query(query, (name,))
                result = db.cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            print("An error occurred while searching for food:", e)
            return None
