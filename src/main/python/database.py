import sqlite3

from services import ItemData, FilterManager


class DatabaseHandler:
    def __init__(self, db_name):
        """Initialize a DatabaseHandler instance.

        Args:
            db_name (str): Name of the SQLite database.
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        """Connect to the SQLite database."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """Create necessary tables if they don't exist."""
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
        """Insert data into the 'items' table.

        Args:
            group_name (str): Group name of the item.
            taste (str): Taste of the item.
            nicotine (int): Nicotine content of the item.
            volume (int): Volume of the item.
            price (int): Price of the item.
            code (str): Code of the item.
            count (int): Count of the item.
        """
        insert_query = """
        INSERT INTO items (group_name, taste, nicotine, volume, price, code, count)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        values = (group_name, taste, nicotine, volume, price, code, count)
        self.cursor.execute(insert_query, values)
        self.conn.commit()

    def insert_item_data(self, data: ItemData):
        """Insert item data into the 'items' table.

        Args:
            data (ItemData): Item data to be inserted.
        """
        insert_query = """
        INSERT INTO items (group_name, taste, nicotine, volume, price, code, count)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        values = (data.group_name, data.taste, data.nicotine, data.volume, data.price, str(data.code), data.count)
        self.cursor.execute(insert_query, values)
        self.conn.commit()

    def update_item_data(self, data: ItemData):
        """Update item data in the 'items' table.

        Args:
            data (ItemData): Updated item data.
        """
        update_query = "UPDATE items " \
                       "SET group_name = ?, taste = ?, nicotine = ?, volume = ?, price = ?, code = ?, count = ? " \
                       "WHERE id = ?;"
        values = (data.group_name, data.taste, data.nicotine, data.volume, data.price, data.code, data.count, data.id_)
        self.cursor.execute(update_query, values)
        self.conn.commit()

    def delete_data_from_items(self, row_id):
        """Delete item data from the 'items' table.

        Args:
            row_id (int): ID of the item data to be deleted.
        """
        delete_query = "DELETE FROM items WHERE id = ?;"
        self.cursor.execute(delete_query, (row_id,))
        self.conn.commit()

    def retrieve_data_from_items(self):
        """Retrieve all item data from the 'items' table.

        Returns:
            List: List of tuples containing item data.
        """
        retrieve_query = "SELECT * FROM items;"
        self.cursor.execute(retrieve_query)
        rows = self.cursor.fetchall()
        return rows

    def retrieve_groups_names(self):
        """Retrieve distinct group names from the 'items' table.

        Returns:
            List: List of tuples containing distinct group names.
        """
        retrieve_query = "SELECT DISTINCT group_name FROM items ORDER BY count DESC;"
        self.cursor.execute(retrieve_query)
        rows = self.cursor.fetchall()
        return rows

    def retrieve_groups_names_with_filters(self, filter_manager: FilterManager):
        """Retrieve distinct group names from the 'items' table based on filters.

        Args:
            filter_manager (FilterManager): FilterManager instance containing filter settings.

        Returns:
            List: List of tuples containing distinct group names.
        """
        retrieve_query = f"""SELECT DISTINCT group_name 
        FROM items 
        WHERE count {'>' if filter_manager.in_stock else '>='} 0  {("AND group_name = '" + filter_manager.group_name + "'") if filter_manager.group_name is not None else ''}
        ORDER BY count DESC;"""
        self.cursor.execute(retrieve_query)
        rows = self.cursor.fetchall()
        return rows

    def retrieve_count_in_group_with_filters(self, group_name, filter_manager: FilterManager):
        """Retrieve the count of items in a group based on filters.

                Args:
                    group_name (str): Group name for filtering.
                    filter_manager (FilterManager): FilterManager instance containing filter settings.

                Returns:
                    int: Number of items in the specified group based on filters.
                """
        retrieve_query = f"""SELECT COUNT(*) AS row_count 
                FROM items 
                WHERE count {'>' if filter_manager.in_stock else '>='} 0  {("AND group_name = '" + group_name + "'") if group_name is not None else ''}"""
        self.cursor.execute(retrieve_query)
        rows = self.cursor.fetchall()
        return rows[0][0]

    def update_item_count_value(self, _id: int, new_value: int):
        """Update the count of an item in the 'items' table.

        Args:
            _id (int): ID of the item.
            new_value (int): New count value.
        """
        update_query = "UPDATE items SET count = ? WHERE id = ?;"
        self.cursor.execute(update_query, (new_value, _id))
        self.conn.commit()

    def retrieve_data_from_items_with_group_name(self):
        """Retrieve all item data from the 'items' table for a specific group.

        Returns:
            List: List of tuples containing item data for the specified group.
        """
        retrieve_query = """
        SELECT *
        FROM items
        ORDER BY count DESC;
        """
        self.cursor.execute(retrieve_query)
        rows = self.cursor.fetchall()
        return rows

    def count_rows_from_all_items(self, group_name):
        """Count the total number of rows (items) in the 'items' table for a specific group.

        Args:
            group_name (str): Group name for filtering.

        Returns:
            int: Total number of rows for the specified group.
        """
        retrieve_query = """
            SELECT COUNT(*)
            FROM items 
        """
        self.cursor.execute(retrieve_query, (group_name,))
        count = self.cursor.fetchall()
        return count

    def retrieve_data_from_items_with_group_name_where_group(self, group_name):
        """Retrieve item data from the 'items' table for a specific group.

        Args:
            group_name (str): Group name for filtering.

        Returns:
            List: List of tuples containing item data for the specified group.
        """
        retrieve_query = """
        SELECT *
            FROM items
            WHERE group_name = ?
            ORDER BY count DESC;
        """
        self.cursor.execute(retrieve_query, (group_name, ))
        rows = self.cursor.fetchall()
        return rows

    def retrieve_items_where_filter_manager(self, filter_manager: FilterManager):
        """Retrieve item data from the 'items' table based on filter settings.

        Args:
            filter_manager (FilterManager): FilterManager instance containing filter settings.

        Returns:
            List: List of tuples containing item data based on filters.
        """
        retrieve_query = f"""
        SELECT *
            FROM items
            WHERE count {'>' if filter_manager.in_stock else '>='} 0  
{("AND group_name = '" + filter_manager.group_name + "'") if filter_manager.group_name is not None else ''}
{("AND LOWER(taste) = '" + filter_manager.search_taste + "%'") if filter_manager.search_taste is not None and len(filter_manager.search_taste) > 2 else ''}  
            ORDER BY count DESC;
        """
        self.cursor.execute(retrieve_query)
        rows = self.cursor.fetchall()
        return rows

    def count_rows_from_items_where_group_name(self, group_name):
        """Count rows from the 'items' table for a specific group.

        Args:
            group_name (str): Group name for filtering.

        Returns:
            int: Number of rows for the specified group.
        """
        retrieve_query = """
            SELECT COUNT(*)
            FROM items
            WHERE group_name = ?
        """
        self.cursor.execute(retrieve_query, (group_name,))
        count = self.cursor.fetchall()
        return count

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()