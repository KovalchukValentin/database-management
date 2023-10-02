from database import DatabaseHandler

if __name__ == "__main__":
    db_handler = DatabaseHandler('database.db')
    db_handler.connect()
    db_handler.create_tables()
    db_handler.close_connection()