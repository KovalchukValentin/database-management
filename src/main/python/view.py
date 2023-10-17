import shutil
import sys
import webbrowser

import pyperclip
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QStandardItem, QStandardItemModel, QIntValidator
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QHeaderView, QFileDialog
from PyQt5 import QtWidgets
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from database import DatabaseHandler
from PyQt5.uic import loadUi

from services import ItemData, path_csv_to_items_data, FilterManager


class MainWindow(QDialog):
    def __init__(self, appctxt, db_handler):
        super(MainWindow, self).__init__()
        loadUi(appctxt.get_resource("main.ui"), self)
        self.setWindowTitle("")
        self.db_handler = db_handler
        self.filter_manager = FilterManager()
        self.appctxt = appctxt

        self.window_import_csv = None
        self.window_item = None

        self.init_menu_btns()
        self.init_tableview()
        self.init_under_tableview_btns()
        self.group_name_comboBox.currentIndexChanged.connect(self.on_combo_selection_change)
        self.show_group_name_comboBox()

    def init_menu_btns(self):
        self.github_btn.clicked.connect(lambda: webbrowser.open("https://github.com/KovalchukValentin"))
        self.in_stock_checkBox.stateChanged.connect(self.on_in_stock_checkBox_state_change)
        self.add_items_btn.clicked.connect(self.press_add_items)
        self.import_csv_btn.clicked.connect(self.press_import_csv)

    def init_tableview(self):
        self.model = QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(['No', 'Group', 'Taste', 'Nicotine', 'Volume', 'Price', 'Code', 'Count'])
        self.tableView.setModel(self.model)
        selection_model = self.tableView.selectionModel()
        selection_model.selectionChanged.connect(self.selection_changed)

    def init_under_tableview_btns(self):
        self.edit_btn.clicked.connect(self.press_edit_item)
        self.plus_one_btn.clicked.connect(self.press_plus_one_to_item)
        self.minus_one_btn.clicked.connect(self.press_minus_one_to_item)
        self.copy_cod_btn.clicked.connect(self.press_copy_cod_of_item)
        self.disable_btns()

    def selection_changed(self, selected, deselected):
        self.enable_btns()

    def disable_btns(self):
        self.edit_btn.setEnabled(False)
        self.plus_one_btn.setEnabled(False)
        self.minus_one_btn.setEnabled(False)
        self.copy_cod_btn.setEnabled(False)

    def enable_btns(self):
        self.edit_btn.setEnabled(True)
        self.plus_one_btn.setEnabled(True)
        self.minus_one_btn.setEnabled(True)
        self.copy_cod_btn.setEnabled(True)

    def press_edit_item(self):
        if self.window_item is None:
            self.window_item = ItemWindow(main_window=self,
                                          appctxt=self.appctxt,
                                          db_handler=self.db_handler,
                                          item_data=self.get_current_row_item_data())
        self.window_item.show()

    def press_plus_one_to_item(self):
        current_count, index = self.get_current_count_and_index_from_model()
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

    def get_current_row_item_data(self) -> ItemData:
        id_ = self.model.item(self.tableView.selectionModel().currentIndex().row(), 0).text()
        group_name = self.model.item(self.tableView.selectionModel().currentIndex().row(), 1).text()
        taste = self.model.item(self.tableView.selectionModel().currentIndex().row(), 2).text()
        nicotine = int(self.model.item(self.tableView.selectionModel().currentIndex().row(), 3).text())
        volume = int(self.model.item(self.tableView.selectionModel().currentIndex().row(), 4).text())
        price = float(self.model.item(self.tableView.selectionModel().currentIndex().row(), 5).text())
        code = self.model.item(self.tableView.selectionModel().currentIndex().row(), 6).text()
        count = int(self.model.item(self.tableView.selectionModel().currentIndex().row(), 7).text())
        return ItemData(id_, group_name, taste, nicotine, volume, price, code, count)

    def update_group_name_comboBox(self):
        self.group_name_comboBox.clear()
        self.show_group_name_comboBox()

    def show_group_name_comboBox(self):
        self.filter_manager.group_name = None
        self.group_name_comboBox.addItem(f'All ({self.db_handler.retrieve_count_in_group_with_filters(None, self.filter_manager)})')
        for row in self.db_handler.retrieve_groups_names_with_filters(self.filter_manager):
            self.group_name_comboBox.addItem(f'{row[0]} ({self.db_handler.retrieve_count_in_group_with_filters(row[0], self.filter_manager)})')

    def on_combo_selection_change(self, index):
        if index == 0:
            self.filter_manager.group_name = None
        else:
            self.filter_manager.group_name = " ".join(self.group_name_comboBox.itemText(index).split()[:-1:])
        self.update_table()

    def on_in_stock_checkBox_state_change(self, state):
        if state == Qt.Checked:
            self.filter_manager.in_stock = True
        else:
            self.filter_manager.in_stock = False
        self.update_group_name_comboBox()
        self.update_table()

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
        if self.window_item is None:
            self.window_item = ItemWindow(main_window=self,
                                          appctxt=self.appctxt,
                                          db_handler=self.db_handler)
        self.window_item.show()

    def remove_rows(self):
        for row in range(self.model.rowCount(), -1, -1):
            self.model.removeRow(row)

    def update_table(self):
        self.remove_rows()
        self.show_data_in_table()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.disable_btns()

    def show_data_in_table(self):
        self.append_rows_to_table_model(self.db_handler.retrieve_items_where_filter_manager(self.filter_manager))

    def press_import_csv(self):
        if self.window_import_csv is None:
            self.window_import_csv = ImportCSVWindow(main_window=self,
                                                     appctxt=self.appctxt,
                                                     db_handler=self.db_handler)
        self.window_import_csv.show()


class ItemWindow(QWidget):
    def __init__(self, main_window: MainWindow, appctxt, db_handler, item_data=ItemData()):
        super().__init__()
        loadUi(appctxt.get_resource("item.ui"), self)
        self.setWindowTitle("Item")

        self.main_window = main_window
        self.db_handler = db_handler
        self.item_data = item_data

        self.cansel_btn.clicked.connect(self.press_cansel)
        self.save_btn.clicked.connect(self.press_save)

        self.init_group_comboBox()

        if not self.item_data.isNew():
            self.show_data()

    def press_save(self):
        self.change_item_data_from_inputs()
        if not self.item_data.isValid():
            return
        if self.item_data.isNew():
            self.db_handler.insert_item_data(self.item_data)
            self.clear()
            self.update_group_comboBox()
        else:
            self.db_handler.update_item_data(self.item_data)
            self.close()

        self.main_window.update_table()
        self.main_window.update_group_name_comboBox()

    def clear(self):
        self.group_edit.setText("")
        self.taste_edit.setText("")
        self.nicotine_spinBox.setValue(0)
        self.volume_spinBox.setValue(0)
        self.price_doubleSpinBox.setValue(0)
        self.code_edit.setText("")
        self.count_spinBox.setValue(0)

    def press_cansel(self):
        self.close()

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

    def update_group_comboBox(self):
        self.group_comboBox.clear()
        self.add_group_names_to_comboBox()

    def add_group_names_to_comboBox(self):
        self.group_comboBox.addItem("Select group")
        for row in self.db_handler.retrieve_groups_names():
            self.group_comboBox.addItem(row[0])

    def on_combo_selection_change(self, index):
        if not self.group_comboBox.currentIndex() == 0:
            self.group_edit.setText(self.group_comboBox.currentText())
            self.group_comboBox.setCurrentIndex(0)

    def show_data(self):
        self.group_edit.setText(self.item_data.group_name)
        self.taste_edit.setText(self.item_data.taste)
        self.nicotine_spinBox.setValue(self.item_data.nicotine)
        self.volume_spinBox.setValue(self.item_data.volume)
        self.price_doubleSpinBox.setValue(self.item_data.price)
        self.code_edit.setText(self.item_data.code)
        self.count_spinBox.setValue(self.item_data.count)


class ImportCSVWindow(QWidget):
    def __init__(self, main_window: MainWindow, appctxt, db_handler):
        super().__init__()
        loadUi(appctxt.get_resource("import_csv.ui"), self)
        self.setWindowTitle("Import CSV")
        self.main_window = main_window
        self.db_handler = db_handler
        self.path_to_example = appctxt.get_resource("example.csv")
        self.init_btns()

    def init_btns(self):
        self.browse_btn.clicked.connect(self.press_browse)
        self.import_csv_btn.clicked.connect(self.press_import_csv)
        self.load_example_btn.clicked.connect(self.press_load_example)

    def press_browse(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.csv);;All Files (*)',
                                                   options=options)
        if file_path:
            self.path_edit.setText(file_path)

    def press_import_csv(self):
        if not self.path_edit.text():
            return
        for item_data in path_csv_to_items_data(self.path_edit.text()):
            if item_data.isValid():
                try:
                    self.db_handler.insert_item_data(item_data)
                except:
                    continue
        self.main_window.update_table()
        self.main_window.update_group_name_comboBox()
        self.close()

    def press_load_example(self):
        options = QFileDialog.Options()
        directory_dialog = QFileDialog()
        directory_path = directory_dialog.getExistingDirectory(self, 'Open Folder', '', options=options)
        if directory_path:
            shutil.copy(self.path_to_example, directory_path + '/' + self.path_to_example.split('\\')[-1])
        self.close()


def main():
    db_handler = DatabaseHandler('database.db')
    db_handler.connect()
    db_handler.create_tables()

    appctxt = ApplicationContext()
    main_window = MainWindow(appctxt, db_handler)

    widget = QtWidgets.QStackedWidget()
    widget.addWidget(main_window)
    widget.setFixedHeight(720)
    widget.setFixedWidth(1280)
    widget.setWindowTitle("Developed By @Valent_nk")
    widget.show()

    try:
        sys.exit(appctxt.app.exec_())
    except ValueError as err:
        db_handler.close_connection()
        print("Exiting" + str(err))
