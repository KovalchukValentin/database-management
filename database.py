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
                   name TEXT UNIQUE
               );
               """

        self.cursor.execute(create_second_table_query)
        self.cursor.execute(create_table_query)

        self.conn.commit()

    def insert_data_to_items(self, group_id: int, taste: str, nicotine: int, volume: int, price: int, code: int, count: int):
        insert_query = """
        INSERT INTO items (group_id, taste, nicotine, volume, price, code, count)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        values = (group_id, taste, nicotine, volume, price, code, count)
        self.cursor.execute(insert_query, values)
        self.conn.commit()

    def insert_data_to_groups(self, values: list):
        insert_query = """
        INSERT INTO groups (name)
        VALUES (?);
        """
        self.cursor.executemany(insert_query, values)
        self.conn.commit()

    def delete_data_from_items(self, row_id):
        delete_query = "DELETE FROM items WHERE id = ?;"
        self.cursor.execute(delete_query, (row_id,))
        self.conn.commit()

    def retrieve_data_from_items(self):
        retrieve_query = "SELECT * FROM items;"
        self.cursor.execute(retrieve_query)
        rows = self.cursor.fetchall()
        return rows

    def retrieve_groups_names(self):

        retrieve_query = "SELECT name FROM groups;"
        self.cursor.execute(retrieve_query)
        rows = self.cursor.fetchall()
        return rows

    def update_item_count_value(self, row_id: int, new_value: int):
        update_query = "UPDATE items SET count = ? WHERE id = ?;"
        self.cursor.execute(update_query, (new_value, row_id))
        self.conn.commit()

    def retrieve_data_from_items_with_group_name(self):
        retrieve_query = """
        SELECT items.id, groups.name, items.taste, items.nicotine, items.volume, items.price, items.code, items.count
        FROM items
        JOIN groups ON items.group_id = groups.id;
        """
        self.cursor.execute(retrieve_query)
        rows = self.cursor.fetchall()
        return rows

    def count_rows_from_all_items(self, group_name):
        retrieve_query = """
            SELECT COUNT(*)
            FROM items
        """
        self.cursor.execute(retrieve_query, (group_name,))
        count = self.cursor.fetchall()
        return count

    def retrieve_data_from_items_with_group_name_where_group(self, group_name):
        retrieve_query = """
        SELECT items.id, groups.name, items.taste, items.nicotine, items.volume, items.price, items.code, items.count
            FROM items
            JOIN groups ON items.group_id = groups.id
            WHERE groups.name = ?
        """
        self.cursor.execute(retrieve_query, (group_name, ))
        rows = self.cursor.fetchall()
        return rows

    def count_rows_from_items_where_group_name(self, group_name):
        retrieve_query = """
            SELECT COUNT(*)
            FROM items
            JOIN groups ON items.group_id = groups.id
            WHERE groups.name = ?
        """
        self.cursor.execute(retrieve_query, (group_name,))
        count = self.cursor.fetchall()
        return count

    def close_connection(self):
        if self.conn:
            self.conn.close()