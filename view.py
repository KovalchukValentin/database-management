import sys
import pyperclip

from PyQt5.QtGui import QStandardItem, QStandardItemModel, QIntValidator
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

        # self.edit_groups_btn.clicked.connect(self.press_edit_groups)
        self.add_items_btn.clicked.connect(self.press_add_items)

        self.edit_btn.clicked.connect(self.press_edit_item)
        self.plus_one_btn.clicked.connect(self.press_plus_one_to_item)
        self.minus_one_btn.clicked.connect(self.press_minus_one_to_item)
        self.copy_cod_btn.clicked.connect(self.press_copy_cod_of_item)

        self.model = QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(['No', 'Group', 'Taste', 'Nicotine', 'Volume', 'Price', 'Code', 'Count'])
        self.tableView.setModel(self.model)

        self.comboBox.currentIndexChanged.connect(self.on_combo_selection_change)
        self.show_left_menu()

    def press_edit_item(self):
        pass

    def press_plus_one_to_item(self):
        current_count = int(self.model.item(self.tableView.selectionModel().currentIndex().row(), 7).text())
        index = int(self.model.item(self.tableView.selectionModel().currentIndex().row(), 0).text())
        self.db_handler.update_item_count_value(index, current_count + 1)

        item_index = self.model.index(self.tableView.selectionModel().currentIndex().row(), 7)
        self.model.setData(item_index, current_count + 1)

    def press_minus_one_to_item(self):
        current_count = int(self.model.item(self.tableView.selectionModel().currentIndex().row(), 7).text())
        if current_count <= 0:
            return
        index = int(self.model.item(self.tableView.selectionModel().currentIndex().row(), 0).text())
        self.db_handler.update_item_count_value(index, current_count - 1)

        item_index = self.model.index(self.tableView.selectionModel().currentIndex().row(), 7)
        self.model.setData(item_index, current_count - 1)

    def press_copy_cod_of_item(self):
        pyperclip.copy(str(self.model.item(self.tableView.selectionModel().currentIndex().row(), 6).text()))

    def get_current_row_data(self) -> list:
        pass

    def show_left_menu(self):
        self.comboBox.addItem("All")
        for row in self.db_handler.retrieve_groups_names():
            self.comboBox.addItem(row[0])

    def on_combo_selection_change(self, index):
        self.remove_rows()
        if self.comboBox.currentText() == "All":
            self.view_all_data_from_db()
        else:
            self.view_group_items_from_db(self.comboBox.currentText())

    def view_all_data_from_db(self):
        data = self.db_handler.retrieve_data_from_items_with_group_name()
        self.append_rows_to_table_model(data)

    def view_group_items_from_db(self, group_name: str):
        data = self.db_handler.retrieve_data_from_items_with_group_name_where_group(group_name)
        self.append_rows_to_table_model(data)

    def append_rows_to_table_model(self, data):
        for row in data:
            self.model.appendRow([QStandardItem(str(i)) for i in row])

    # def press_edit_groups(self):
    #     if self.window_add_group is None:
    #         self.window_add_group = EditGroupsWindow(self.db_handler)
    #     self.window_add_group.show()

    def press_add_items(self):
        if self.window_add_items is None:
            self.window_add_items = ItemWindow(self.db_handler)
        self.window_add_items.show()

    def remove_rows(self):
        for row in range(self.model.rowCount(), -1, -1):
            self.model.removeRow(row)


# class EditGroupsWindow(QWidget):
#     def __init__(self, db_handler):
#         super().__init__()
#         self.db_handler = db_handler
#         loadUi("add_groups.ui", self)
#         self.setWindowTitle("Edit groups")
#         self.model = QStandardItemModel(self)
#         self.model.setHorizontalHeaderLabels(["Name", ])
#         self.tableView.setModel(self.model)
#
#         self.save_btn.clicked.connect(self.press_save)
#         self.new_btn.clicked.connect(self.press_new)
#         self.delete_btn.clicked.connect(self.press_delete)
#
#         self.show_groups()
#
#     def show_groups(self):
#         for row in self.db_handler.retrieve_groups_names():
#             self.model.appendRow([QStandardItem(str(i)) for i in row])
#
#     # def press_new(self):
#     #     self.model.appendRow([QStandardItem(""), ])
#
#     # def press_delete(self):
#     #     current_index = self.tableView.currentIndex()
#     #
#     #     # Check if an item is selected
#     #     if current_index.isValid():
#     #         # Remove the row corresponding to the selected item
#     #         self.model.removeRow(current_index.row())
#
#     # def press_save(self):
#     #     data = []
#     #
#     #     for row in range(self.model.rowCount()):
#     #         item = self.model.item(row, 0)
#     #         if item is not None:
#     #             print(item.text())
#     #             data.append([item.text()])
#     #         else:
#     #             data.append(None)
#     #
#     #     if data:
#     #         self.db_handler.insert_data_to_groups(data)
#     #     self.remove_rows()
#     #     self.close()
#
#     def remove_rows(self):
#         for row in range(self.model.rowCount(), -1, -1):
#             self.model.removeRow(row)


class ItemWindow(QWidget):
    def __init__(self, db_handler, data=None):
        super().__init__()
        self.db_handler = db_handler
        self.data = data

        self.setWindowTitle("Item")
        loadUi("item.ui", self)

        self.cansel_btn.clicked.connect(self.press_cansel)
        self.save_btn.clicked.connect(self.press_save)

    def press_save(self):
        self.get_data_from_inputs()

    def press_cansel(self):
        pass

    def get_data_from_inputs(self):
        result = (self.group_edit.text(),
        self.taste_edit.text(),
        self.nicotine_spinBox.value(),
        self.volume_spinBox.value(),
        self.price_doubleSpinBox.value(),
        self.code_edit.text(),
        self.count_spinBox.value())
        return result




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
    widget.show()

    try:
        sys.exit(app.exec_())
    except ValueError as err:
        db_handler.close_connection()
        print("Exiting" + str(err))


def view_all_in_terminal(db_handler: DatabaseHandler):
    data = db_handler.retrieve_data_from_items_with_group_name()
    print("Data retrieved from the database:")
    for row in data:
        print(row)
