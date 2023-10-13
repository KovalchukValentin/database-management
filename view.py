import sys
import pyperclip

from PyQt5.QtGui import QStandardItem, QStandardItemModel, QIntValidator
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5 import QtWidgets

from database import DatabaseHandler
from PyQt5.uic import loadUi

from services import ItemData


class MainWindow(QDialog):
    def __init__(self, db_handler):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Database")
        self.db_handler = db_handler
        loadUi("main.ui", self)
        self.window_add_group = None
        self.window_add_items = None

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
        current_count, index = self.get_current_count_and_index_from_model()
        print(current_count, index)
        self.db_handler.update_item_count_value(index, current_count + 1)

        item_index = self.model.index(self.tableView.selectionModel().currentIndex().row(), 7)
        self.model.setData(item_index, current_count + 1)

    def press_minus_one_to_item(self):
        current_count, index = self.get_current_count_and_index_from_model()
        if current_count <= 0:
            return

        self.db_handler.update_item_count_value(index, current_count - 1)

        item_index = self.model.index(self.tableView.selectionModel().currentIndex().row(), 7)
        self.model.setData(item_index, current_count - 1)

    def get_current_count_and_index_from_model(self):
        return int(self.model.item(self.tableView.selectionModel().currentIndex().row(), 7).text()), \
               int(self.model.item(self.tableView.selectionModel().currentIndex().row(), 0).text())

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

    def press_add_items(self):
        if self.window_add_items is None:
            self.window_add_items = ItemWindow(self.db_handler)
        self.window_add_items.show()

    def remove_rows(self):
        for row in range(self.model.rowCount(), -1, -1):
            self.model.removeRow(row)


class ItemWindow(QWidget):
    def __init__(self, db_handler, item_data=ItemData()):
        super().__init__()
        self.db_handler = db_handler
        self.item_data = item_data
        self.isEditor = self.item_data.isNew()

        self.setWindowTitle("Item")
        loadUi("item.ui", self)

        self.cansel_btn.clicked.connect(self.press_cansel)
        self.save_btn.clicked.connect(self.press_save)

        self.init_group_comboBox()

    def press_save(self):
        self.change_item_data_from_inputs()
        if not self.item_data.isValid():
            return
        if self.item_data.isNew():
            self.db_handler.insert_item_data(self.item_data)
        else:
            self.db_handler.update_item_data(self.item_data)
        self.clear()

    def clear(self):
        self.group_edit.setText("")
        self.taste_edit.setText("")
        self.nicotine_spinBox.setValue(0)
        self.volume_spinBox.setValue(0)
        self.price_doubleSpinBox.setValue(0)
        self.code_edit.setText("")
        self.count_spinBox.setValue(0)

    def press_cansel(self):
        pass

    def change_item_data_from_inputs(self):
        self.item_data.setData(group_name=self.group_edit.text(),
                               taste=self.taste_edit.text(),
                               nicotine=self.nicotine_spinBox.value(),
                               volume=self.volume_spinBox.value(),
                               price=self.price_doubleSpinBox.value(),
                               code=self.code_edit.text(),
                               count=self.count_spinBox.value())

    def init_group_comboBox(self):
        self.group_comboBox.currentIndexChanged.connect(self.on_combo_selection_change)
        self.add_group_names_to_comboBox()

    def add_group_names_to_comboBox(self):
        self.group_comboBox.addItem("Select group")
        for row in self.db_handler.retrieve_groups_names():
            self.group_comboBox.addItem(row[0])

    def on_combo_selection_change(self, index):
        if not self.group_comboBox.currentIndex() == 0:
            self.group_edit.setText(self.group_comboBox.currentText())
            self.group_comboBox.setCurrentIndex(0)


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
