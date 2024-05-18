import sqlite3


class SQLiteDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

    def fetch_all(self, query, *args, **kwargs):
        cursor = self.connection.cursor()
        cursor.execute(query, *args, **kwargs)
        res = cursor.fetchall()
        if res:
            return res
        return None

    def fetch_one(self, query, *args, **kwargs):
        cursor = self.connection.cursor()
        cursor.execute(query, *args, **kwargs)
        res = cursor.fetchone()
        if res:
            return res
        return None

    def execute(self, query, *args, **kwargs):
        cursor = self.connection.cursor()
        cursor.execute(query, *args, **kwargs)
        self.connection.commit()
