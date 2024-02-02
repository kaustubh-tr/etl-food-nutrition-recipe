import psycopg2
from config.config import Config

class DBConnector:
    def __init__(self):
        self.conn = psycopg2.connect(
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=Config.DB_PORT
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query, values=None):
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
                
            self.conn.commit()
        except Exception as e:
            print("Error executing query:", e)
            self.conn.rollback()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_connection()
