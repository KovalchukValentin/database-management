import sys

from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5 import QtWidgets

from database import DatabaseHandler
from PyQt5.uic import loadUi


class MainWindow(QDialog):
    def __init__(self, db_handler):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Database")
        self.db_handler = db_handler
        loadUi("main.ui", self)
        self.window_add_group = None
        self.window_add_items = None

        self.add_group_btn.clicked.connect(self.press_add_groups)
        self.add_items_btn.clicked.connect(self.press_add_items)

        self.model = QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(['No', 'Group', 'Taste', 'Nicotine', 'Volume', 'Price', 'Code', 'Count'])
        self.tableView.setModel(self.model)
        # self.tableView.setEditTriggers(QTableView.NoEditTriggers)

    def view_all_data_from_bd(self):

        data = self.db_handler.retrieve_data_from_items_with_group_name()
        # self.tableView.append("Data retrieved from the database:")
        for row in data:
            self.model.appendRow([QStandardItem(str(i)) for i in row])

    def press_add_groups(self):
        if self.window_add_group is None:
            self.window_add_group = AddGroupsWindow()
        self.window_add_group.show()

    def press_add_items(self):
        if self.window_add_items is None:
            self.window_add_items = AddItemsWindow()
        self.window_add_items.show()


class AddGroupsWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("add_groups.ui", self)
        self.setWindowTitle("Add groups")
        self.model = QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(["Name", ])
        self.tableView.setModel(self.model)

        self.save_btn.clicked.connect(self.press_new)
        self.new_btn.clicked.connect(self.press_new)

    def press_new(self):
        self.model.appendRow([QStandardItem(""), ])


class AddItemsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add items")


def main():
    db_handler = DatabaseHandler('database.db')
    db_handler.connect()
    db_handler.create_tables()

    view_all_in_terminal(db_handler)

    app = QApplication(sys.argv)
    main_window = MainWindow(db_handler)

    widget = QtWidgets.QStackedWidget()
    widget.addWidget(main_window)
    widget.setFixedHeight(720)
    widget.setFixedWidth(1280)
    main_window.view_all_data_from_bd()
    widget.show()

    try:
        sys.exit(app.exec_())
    except ValueError:
        db_handler.close_connection()
        print("Exiting")


def view_all_in_terminal(db_handler: DatabaseHandler):
    data = db_handler.retrieve_data_from_items_with_group_name()
    print("Data retrieved from the database:")
    for row in data:
        print(row)
