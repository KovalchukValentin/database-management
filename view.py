from database import DatabaseHandler


def main():
    db_handler = DatabaseHandler('database.db')
    db_handler.connect()
    db_handler.create_tables()

    view_all_in_terminal(db_handler)

    db_handler.close_connection()


def view_all_in_terminal(db_handler:DatabaseHandler):
    data = db_handler.retrieve_data()
    print("Data retrieved from the database:")
    for row in data:
        print(row)
