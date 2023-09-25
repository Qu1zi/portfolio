import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("details.db")
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT
            )
        """)
        self.conn.commit()

    def add_detail(self, name, description):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO details (name, description) VALUES (?, ?)", (name, description))
        self.conn.commit()

    def get_details(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name FROM details")
        return cursor.fetchall()

    def get_detail(self, detail_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, description FROM details WHERE id=?", (detail_id,))
        return cursor.fetchone()

    def delete_detail(self, detail_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM details WHERE id=?", (detail_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()