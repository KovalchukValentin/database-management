import sqlite3

from services import ItemData


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
            group_name TEXT,
            taste TEXT,
            nicotine INTEGER,
            volume INTEGER,
            price REAL,
            code TEXT UNIQUE,
            count INTEGER
        );
        """

        self.cursor.execute(create_table_query)

        self.conn.commit()

    def insert_data_to_items(self, group_name: str, taste: str, nicotine: int, volume: int, price: int, code: str, count: int):
        insert_query = """
        INSERT INTO items (group_name, taste, nicotine, volume, price, code, count)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        values = (group_name, taste, nicotine, volume, price, code, count)
        self.cursor.execute(insert_query, values)
        self.conn.commit()

    def insert_item_data(self, data: ItemData):
        insert_query = """
        INSERT INTO items (group_name, taste, nicotine, volume, price, code, count)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        values = (data.group_name, data.taste, data.nicotine, data.volume, data.price, str(data.code), data.count)
        self.cursor.execute(insert_query, values)
        self.conn.commit()

    def update_item_data(self, data: ItemData):
        update_query = "UPDATE items " \
                       "SET group_name = ?, taste = ?, nicotine = ?, volume = ?, price = ?, code = ?, count = ? " \
                       "WHERE id = ?;"
        values = (data.group_name, data.taste, data.nicotine, data.volume, data.price, data.code, data.count, data.id_)
        self.cursor.execute(update_query, values)
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
        retrieve_query = "SELECT DISTINCT group_name FROM items ORDER BY count DESC;"
        self.cursor.execute(retrieve_query)
        rows = self.cursor.fetchall()
        return rows

    def update_item_count_value(self, _id: int, new_value: int):
        update_query = "UPDATE items SET count = ? WHERE id = ?;"
        self.cursor.execute(update_query, (new_value, _id))
        self.conn.commit()

    def retrieve_data_from_items_with_group_name(self):
        retrieve_query = """
        SELECT *
        FROM items
        ORDER BY count DESC;
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
        SELECT *
            FROM items
            WHERE group_name = ?
            ORDER BY count DESC;
        """
        self.cursor.execute(retrieve_query, (group_name, ))
        rows = self.cursor.fetchall()
        return rows

    def count_rows_from_items_where_group_name(self, group_name):
        retrieve_query = """
            SELECT COUNT(*)
            FROM items
            WHERE group_name = ?
        """
        self.cursor.execute(retrieve_query, (group_name,))
        count = self.cursor.fetchall()
        return count

    def close_connection(self):
        if self.conn:
            self.conn.close()