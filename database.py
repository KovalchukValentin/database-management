import sqlite3


class DatabaseHandler:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS sets (
            id INTEGER PRIMARY KEY,
            brand TEXT,
            taste TEXT,
            nicotine INTEGER,
            volume INTEGER,
            price INTEGER,
            code INTEGER UNIQUE,
            count INTEGER
        );
        """
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def insert_data(self, brand: str, taste: str, nicotine: int, volume: int, price: int, code: int, count: int):
        insert_query = """
        INSERT INTO sets (brand, taste, nicotine, volume, price, code, count)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        values = (brand, taste, nicotine, volume, price, code, count)
        self.cursor.execute(insert_query, values)
        self.conn.commit()

    def delete_data(self, row_id):
        delete_query = "DELETE FROM sets WHERE id = ?;"
        self.cursor.execute(delete_query, (row_id,))
        self.conn.commit()

    def retrieve_data(self):
        retrieve_query = "SELECT * FROM sets;"
        self.cursor.execute(retrieve_query)
        rows = self.cursor.fetchall()
        return rows

    def update_count_value(self, row_id: int, new_value: int):
        update_query = "UPDATE my_table SET count = ? WHERE id = ?;"
        self.cursor.execute(update_query, (new_value, row_id))
        self.conn.commit()

    def close_connection(self):
        if self.conn:
            self.conn.close()