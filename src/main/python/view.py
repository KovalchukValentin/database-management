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
from language import Language
from setting import Settings
from style import Theme


class MainWindow(QDialog):
    def __init__(self, appctxt, db_handler):
        # Constructor for the MainWindow class
        # Initializes the main window with the provided parameters
        # Loads the UI from a file using appctxt and sets up event connections
        super(MainWindow, self).__init__()
        loadUi(appctxt.get_resource("main.ui"), self)
        self.language = Language(Settings().language)
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
        self.update_language()

        self.setStyleSheet(Theme(Settings().theme).get_theme())

    def init_menu_btns(self):
        # Initializes menu buttons and sets up event connections

        self.github_btn.clicked.connect(lambda: webbrowser.open("https://github.com/KovalchukValentin"))
        self.in_stock_checkBox.stateChanged.connect(self.on_in_stock_checkBox_state_change)
        self.add_items_btn.clicked.connect(self.press_add_items)
        self.import_csv_btn.clicked.connect(self.press_import_csv)

    def init_tableview(self):
        # Initializes the table view
        self.model = QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(['No',
                                              self.language.group,
                                              self.language.taste,
                                              self.language.nicotine,
                                              self.language.volume,
                                              self.language.price,
                                              self.language.cod,
                                              self.language.count])
        self.tableView.setModel(self.model)
        selection_model = self.tableView.selectionModel()
        selection_model.selectionChanged.connect(self.selection_changed)

    def init_under_tableview_btns(self):
        # Initializes buttons below the table view and sets up event connections
        self.edit_btn.clicked.connect(self.press_edit_item)
        self.plus_one_btn.clicked.connect(self.press_plus_one_to_item)
        self.minus_one_btn.clicked.connect(self.press_minus_one_to_item)
        self.copy_cod_btn.clicked.connect(self.press_copy_cod_of_item)
        self.disable_btns()

    def selection_changed(self, selected, deselected):
        # Handler for table view selection change
        # Enables or disables buttons based on selection
        self.enable_btns()

    def disable_btns(self):
        # Disables specific buttons in the UI
        self.edit_btn.setEnabled(False)
        self.plus_one_btn.setEnabled(False)
        self.minus_one_btn.setEnabled(False)
        self.copy_cod_btn.setEnabled(False)

    def enable_btns(self):
        # Enables specific buttons in the UI
        self.edit_btn.setEnabled(True)
        self.plus_one_btn.setEnabled(True)
        self.minus_one_btn.setEnabled(True)
        self.copy_cod_btn.setEnabled(True)

    def press_edit_item(self):
        # Handler for edit item button press
        # Opens an ItemWindow to edit the selected item
        if self.window_item is None:
            self.window_item = ItemWindow(main_window=self,
                                          appctxt=self.appctxt,
                                          db_handler=self.db_handler,
                                          item_data=self.get_current_row_item_data())
        self.window_item.show()

    def press_plus_one_to_item(self):
        # Handler for plus one button press
        # Increases item count by one in the database and updates the UI
        current_count, index = self.get_current_count_and_index_from_model()
        self.db_handler.update_item_count_value(index, current_count + 1)

        item_index = self.model.index(self.tableView.selectionModel().currentIndex().row(), 7)
        self.model.setData(item_index, current_count + 1)

    def press_minus_one_to_item(self):
        # Handler for minus one button press
        # Decreases item count by one in the database and updates the UI
        current_count, index = self.get_current_count_and_index_from_model()
        if current_count <= 0:
            return

        self.db_handler.update_item_count_value(index, current_count - 1)

        item_index = self.model.index(self.tableView.selectionModel().currentIndex().row(), 7)
        self.model.setData(item_index, current_count - 1)

    def get_current_count_and_index_from_model(self):
        # Retrieves the current item count and index from the table view
        return int(self.model.item(self.tableView.selectionModel().currentIndex().row(), 7).text()), \
               int(self.model.item(self.tableView.selectionModel().currentIndex().row(), 0).text())

    def press_copy_cod_of_item(self):
        # Handler for copy code button press
        # Copies the item code to the clipboard
        pyperclip.copy(str(self.model.item(self.tableView.selectionModel().currentIndex().row(), 6).text()))

    def get_current_row_item_data(self) -> ItemData:
        # Retrieves item data from the current selected row in the table view
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
        # Updates the group name ComboBox
        self.group_name_comboBox.clear()
        self.show_group_name_comboBox()

    def show_group_name_comboBox(self):
        # Shows group names in the ComboBox
        self.filter_manager.group_name = None
        self.group_name_comboBox.addItem(f'{self.language.all} ({self.db_handler.retrieve_count_in_group_with_filters(None, self.filter_manager)})')
        for row in self.db_handler.retrieve_groups_names_with_filters(self.filter_manager):
            self.group_name_comboBox.addItem(f'{row[0]} ({self.db_handler.retrieve_count_in_group_with_filters(row[0], self.filter_manager)})')

    def on_combo_selection_change(self, index):
        # Handler for group name ComboBox selection change
        # Updates the table based on the selected group
        if index == 0:
            self.filter_manager.group_name = None
        else:
            self.filter_manager.group_name = " ".join(self.group_name_comboBox.itemText(index).split()[:-1:])
        self.update_table()

    def on_in_stock_checkBox_state_change(self, state):
        # Handler for in-stock CheckBox state change
        # Updates the group name ComboBox and table based on the CheckBox state
        if state == Qt.Checked:
            self.filter_manager.in_stock = True
        else:
            self.filter_manager.in_stock = False
        self.update_group_name_comboBox()
        self.update_table()

    def view_all_data_from_db(self):
        # Retrieves and displays all data from the database
        data = self.db_handler.retrieve_data_from_items_with_group_name()
        self.append_rows_to_table_model(data)

    def view_group_items_from_db(self, group_name: str):
        # Retrieves and displays items from the database for a specific group
        data = self.db_handler.retrieve_data_from_items_with_group_name_where_group(group_name)
        self.append_rows_to_table_model(data)

    def append_rows_to_table_model(self, data):
        # Appends rows to the table model for display in the table view
        for row in data:
            self.model.appendRow([QStandardItem(str(i)) for i in row])

    def press_add_items(self):
        # Handler for add items button press
        # Opens an ItemWindow to add new items
        if self.window_item is None:
            self.window_item = ItemWindow(main_window=self,
                                          appctxt=self.appctxt,
                                          db_handler=self.db_handler)
        self.window_item.show()

    def remove_rows(self):
        # Removes all rows from the table view
        for row in range(self.model.rowCount(), -1, -1):
            self.model.removeRow(row)

    def update_table(self):
        # Updates the table view with the latest data
        self.remove_rows()
        self.show_data_in_table()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.disable_btns()

    def show_data_in_table(self):
        # Shows data in the table view
        self.append_rows_to_table_model(self.db_handler.retrieve_items_where_filter_manager(self.filter_manager))

    def press_import_csv(self):
        # Handler for import CSV button press
        # Opens an ImportCSVWindow to import CSV data
        if self.window_import_csv is None:
            self.window_import_csv = ImportCSVWindow(main_window=self,
                                                     appctxt=self.appctxt,
                                                     db_handler=self.db_handler)
        self.window_import_csv.show()

    def update_language(self):
        self.in_stock_checkBox.setText(self.language.only_in_stock)
        self.add_items_btn.setText(self.language.add_items)
        self.edit_btn.setText(self.language.edit)
        self.copy_cod_btn.setText(self.language.cod)


class ItemWindow(QWidget):
    def __init__(self, main_window: MainWindow, appctxt, db_handler, item_data=ItemData()):
        # Constructor for the ItemWindow class
        # Initializes the ItemWindow with the provided parameters
        # Loads the UI from a file using appctxt and sets up event connections
        super().__init__()
        loadUi(appctxt.get_resource("item.ui"), self)
        self.language = Language(Settings().language)
        self.setWindowTitle(self.language.item)

        self.main_window = main_window
        self.db_handler = db_handler
        self.item_data = item_data

        self.cansel_btn.clicked.connect(self.press_cansel)
        self.save_btn.clicked.connect(self.press_save)

        self.init_group_comboBox()

        if not self.item_data.isNew():
            self.show_data()

        self.update_language()
        self.setStyleSheet(Theme(Settings().theme).get_theme())

    def press_save(self):
        # Handler for save button press
        # Extracts data from UI inputs, validates it, and either inserts or updates item data in the database
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
        # Clears the UI input fields
        self.group_edit.setText("")
        self.taste_edit.setText("")
        self.nicotine_spinBox.setValue(0)
        self.volume_spinBox.setValue(0)
        self.price_doubleSpinBox.setValue(0)
        self.code_edit.setText("")
        self.count_spinBox.setValue(0)

    def press_cansel(self):
        # Handler for cancel button press
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
        # Initializes the group ComboBox and sets up event connection
        self.group_comboBox.currentIndexChanged.connect(self.on_combo_selection_change)
        self.add_group_names_to_comboBox()

    def update_group_comboBox(self):
        # Updates the group ComboBox content
        self.group_comboBox.clear()
        self.add_group_names_to_comboBox()

    def add_group_names_to_comboBox(self):
        # Populates the group ComboBox with group names from the database
        self.group_comboBox.addItem(self.language.select_group)
        for row in self.db_handler.retrieve_groups_names():
            self.group_comboBox.addItem(row[0])

    def on_combo_selection_change(self, index):
        # Handler for ComboBox selection change
        # Updates UI based on ComboBox selection
        if not self.group_comboBox.currentIndex() == 0:
            self.group_edit.setText(self.group_comboBox.currentText())
            self.group_comboBox.setCurrentIndex(0)

    def show_data(self):
        self.setWindowTitle(f"{self.language.item} #{self.item_data.id_}")
        # Displays item data in the UI input fields
        self.group_edit.setText(self.item_data.group_name)
        self.taste_edit.setText(self.item_data.taste)
        self.nicotine_spinBox.setValue(self.item_data.nicotine)
        self.volume_spinBox.setValue(self.item_data.volume)
        self.price_doubleSpinBox.setValue(self.item_data.price)
        self.code_edit.setText(self.item_data.code)
        self.count_spinBox.setValue(self.item_data.count)

    def closeEvent(self, event) -> None:
        self.main_window.window_item = None

    def update_language(self):
        self.group_label.setText(self.language.group)
        self.taste_label.setText(self.language.taste)
        self.nicotine_label.setText(self.language.nicotine)
        self.volume_label.setText(self.language.volume)
        self.price_label.setText(self.language.price)
        self.cod_label.setText(self.language.cod)
        self.count_label.setText(self.language.count)
        self.cansel_btn.setText(self.language.cansel)
        self.save_btn.setText(self.language.save)


class ImportCSVWindow(QWidget):
    def __init__(self, main_window: MainWindow, appctxt, db_handler):
        # Constructor for the ImportCSVWindow class
        # Initializes the window with the provided parameters
        # Loads the UI from a file using appctxt and sets up event connections
        super().__init__()
        loadUi(appctxt.get_resource("import_csv.ui"), self)
        self.language = Language(Settings().language)
        self.setWindowTitle("Import CSV")
        self.main_window = main_window
        self.db_handler = db_handler
        self.path_to_example = appctxt.get_resource("example.csv")
        self.init_btns()
        self.update_language()
        self.setStyleSheet(Theme(Settings().theme).get_theme())

    def init_btns(self):
        # Initializes buttons and sets up event connections
        self.browse_btn.clicked.connect(self.press_browse)
        self.import_csv_btn.clicked.connect(self.press_import_csv)
        self.load_example_btn.clicked.connect(self.press_load_example)

    def press_browse(self):
        # Handler for browse button press
        # Opens a file dialog for selecting a CSV file
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open File', '', 'CSV Files (*.csv);;All Files (*)',
                                                   options=options)
        if file_path:
            self.path_edit.setText(file_path)

    def press_import_csv(self):
        # Handler for import CSV button press
        # Imports CSV data, validates it, and inserts item data into the database
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
        # Handler for load example button press
        # Allows users to load an example CSV file
        options = QFileDialog.Options()
        directory_dialog = QFileDialog()
        directory_path = directory_dialog.getExistingDirectory(self, 'Open Folder', '', options=options)
        if directory_path:
            shutil.copy(self.path_to_example, directory_path + '/' + self.path_to_example.split('\\')[-1])
        self.close()

    def closeEvent(self, event) -> None:
        self.main_window.window_import_csv = None

    def update_language(self):
        self.load_example_btn.setText(self.language.load_example)
        self.browse_btn.setText(self.language.browse)


def main():
    db_handler = DatabaseHandler('database.db')
    db_handler.connect()
    db_handler.create_tables()

    appctxt = ApplicationContext()
    main_window = MainWindow(appctxt, db_handler)

    widget = QtWidgets.QStackedWidget()
    widget.addWidget(main_window)
    widget.setFixedHeight(1280)
    widget.setFixedWidth(1920)
    widget.move(0, 0)
    widget.setWindowTitle("Developed By @Valent_nk")
    widget.show()

    try:
        sys.exit(appctxt.app.exec_())
    except ValueError as err:
        db_handler.close_connection()
        print("Exiting" + str(err))
