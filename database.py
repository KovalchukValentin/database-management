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
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            group_id INTEGER,
            taste TEXT,
            nicotine INTEGER,
            volume INTEGER,
            price INTEGER,
            code INTEGER UNIQUE,
            count INTEGER,
            FOREIGN KEY (group_id) REFERENCES groups(id)
            
        );
        """

        create_second_table_query = """
               CREATE TABLE IF NOT EXISTS groups (
                   id INTEGER PRIMARY KEY,
                   data TEXT
               );
               """

        self.cursor.execute(create_second_table_query)
        self.cursor.execute(create_table_query)

        self.conn.commit()

    def insert_data(self, group_id: str, taste: str, nicotine: int, volume: int, price: int, code: int, count: int):
        insert_query = """
        INSERT INTO items (group_id, taste, nicotine, volume, price, code, count)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        values = (group_id, taste, nicotine, volume, price, code, count)
        self.cursor.execute(insert_query, values)
        self.conn.commit()

    def delete_data(self, row_id):
        delete_query = "DELETE FROM items WHERE id = ?;"
        self.cursor.execute(delete_query, (row_id,))
        self.conn.commit()

    def retrieve_data(self):
        retrieve_query = "SELECT * FROM items;"
        self.cursor.execute(retrieve_query)
        rows = self.cursor.fetchall()
        return rows

    def update_item_count_value(self, row_id: int, new_value: int):
        update_query = "UPDATE items SET count = ? WHERE id = ?;"
        self.cursor.execute(update_query, (new_value, row_id))
        self.conn.commit()

    def close_connection(self):
        if self.conn:
            self.conn.close()