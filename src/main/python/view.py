import os
import shutil
import subprocess
import sys
import webbrowser

import pyperclip
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QStandardItem, QStandardItemModel, QIntValidator, QKeySequence
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QHeaderView, QFileDialog, QMainWindow, QShortcut
from PyQt5 import QtWidgets
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from database import DatabaseHandler
from PyQt5.uic import loadUi

from services import ItemData, FilterManager, CSVImporter, CSVExporter
from language import Language
from setting import Settings
from logger import Logger
from style import Theme


class MainWindow(QMainWindow):
    def __init__(self, appctxt, db_handler):
        # Constructor for the MainWindow class
        # Initializes the main window with the provided parameters
        # Loads the UI from a file using appctxt and sets up event connections
        super(MainWindow, self).__init__()
        loadUi(appctxt.get_resource("main.ui"), self)
        self.language = Language(Settings().language)
        self.logger = Logger()
        self.db_handler = db_handler
        self.filter_manager = FilterManager()
        self.appctxt = appctxt
        self.setFixedHeight(975)
        self.setFixedWidth(1680)

        self.init_windows()
        self.init_menu_btns()
        self.init_tableview()
        self.init_shortcuts()
        self.init_under_tableview_btns()

        self.group_name_comboBox.currentIndexChanged.connect(self.on_combo_selection_change)
        self.search_edit.textChanged.connect(self.on_search_edit_changed)
        self.show_group_name_comboBox()
        self.update_language()

        self.setStyleSheet(Theme(Settings().theme).get_theme())

    def init_windows(self):
        self.window_import_csv = None
        self.window_item = None
        self.window_setting = None
        self.done_window = None

    def init_menu_btns(self):
        # Initializes menu buttons and sets up event connections
        self.actionNew_items.triggered.connect(self.press_add_items)
        self.actionImport_CSV.triggered.connect(self.press_import_csv)
        self.actionExport_All.triggered.connect(self.press_export_all_csv)
        self.actionExport_current_table.triggered.connect(self.press_export_table_csv)
        self.github_btn.clicked.connect(lambda: webbrowser.open("https://github.com/KovalchukValentin"))
        self.in_stock_checkBox.stateChanged.connect(self.on_in_stock_checkBox_state_change)
        self.action_Settings.triggered.connect(self.press_settings)
        self.actionLogs.triggered.connect(self.press_logs)
        self.actionBackup_now.triggered.connect(self.press_backup_now)
        self.actionShow_Backups.triggered.connect(self.press_show_backup)

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
        selection_model.selectionChanged.connect(self.on_selection_changed)

    def init_under_tableview_btns(self):
        # Initializes buttons below the table view and sets up event connections
        self.edit_btn.clicked.connect(self.press_edit_item)
        self.plus_one_btn.clicked.connect(self.press_plus_one_to_item)
        self.minus_one_btn.clicked.connect(self.press_minus_one_to_item)
        self.copy_cod_btn.clicked.connect(self.press_copy_cod_of_item)
        self.disable_btns()

    def init_shortcuts(self):
        QShortcut(QKeySequence('Ctrl+N'), self).activated.connect(self.press_add_items)
        QShortcut(QKeySequence('Ctrl+S'), self).activated.connect(self.press_export_all_csv)
        QShortcut(QKeySequence('Ctrl+Shift+S'), self).activated.connect(self.press_export_all_csv)
        QShortcut(QKeySequence('Ctrl+F'), self).activated.connect(self.search_edit.setFocus)

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

    def get_item_data_from_table_view(self) -> ItemData:
        return ItemData(id_=int(self.model.item(self.tableView.selectionModel().currentIndex().row(), 0).text()),
                        group_name=self.model.item(self.tableView.selectionModel().currentIndex().row(), 1).text(),
                        taste=self.model.item(self.tableView.selectionModel().currentIndex().row(), 2).text(),
                        nicotine=int(self.model.item(self.tableView.selectionModel().currentIndex().row(), 3).text()),
                        volume=int(self.model.item(self.tableView.selectionModel().currentIndex().row(), 4).text()),
                        price=float(self.model.item(self.tableView.selectionModel().currentIndex().row(), 5).text()),
                        code=self.model.item(self.tableView.selectionModel().currentIndex().row(), 6).text(),
                        count=int(self.model.item(self.tableView.selectionModel().currentIndex().row(), 7).text()))

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

    def show_group_name_comboBox(self):
        # Shows group names in the ComboBox
        self.filter_manager.group_name = None
        self.group_name_comboBox.addItem(f'{self.language.all} ({self.db_handler.retrieve_count_in_group_with_filters(None, self.filter_manager)})')
        for row in self.db_handler.retrieve_groups_names_with_filters(self.filter_manager):
            self.group_name_comboBox.addItem(f'{row[0]} ({self.db_handler.retrieve_count_in_group_with_filters(row[0], self.filter_manager)})')

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

    def get_dir_from_file_dialog(self, title: str):
        options = QFileDialog.Options()
        directory_dialog = QFileDialog()
        return directory_dialog.getExistingDirectory(self, title, '', options=options)

    def remove_rows(self):
        # Removes all rows from the table view
        for row in range(self.model.rowCount(), -1, -1):
            self.model.removeRow(row)

    def show_data_in_table(self):
        # Shows data in the table view
        self.append_rows_to_table_model(self.db_handler.retrieve_items_where_filter_manager(self.filter_manager))

    def on_selection_changed(self, selected, deselected):
        # Handler for table view selection change
        # Enables or disables buttons based on selection
        self.enable_btns()

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

    def on_search_edit_changed(self, text):
        if len(text) > 0:
            self.filter_manager.search_taste = text
        else:
            self.filter_manager.search_taste = None
        self.update_table()
        self.update_group_name_comboBox()

    def press_add_items(self):
        # Handler for add items button press
        # Opens an ItemWindow to add new items
        if self.window_item is None:
            self.window_item = ItemWindow(main_window=self,
                                          appctxt=self.appctxt,
                                          db_handler=self.db_handler)
        self.window_item.show()

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
        item_data = self.get_item_data_from_table_view()
        item_data.count += 1
        self.db_handler.update_item_count_value(item_data.id_, item_data.count)

        item_index = self.model.index(self.tableView.selectionModel().currentIndex().row(), 7)
        self.model.setData(item_index, item_data.count)

        self.logger.add_log(f"+1 RESULT: {item_data}")

    def press_minus_one_to_item(self):
        # Handler for minus one button press
        # Decreases item count by one in the database and updates the UI
        item_data = self.get_item_data_from_table_view()
        if item_data.count <= 0:
            return
        item_data.count -= 1
        self.db_handler.update_item_count_value(item_data.id_, item_data.count)

        item_index = self.model.index(self.tableView.selectionModel().currentIndex().row(), 7)
        self.model.setData(item_index, item_data.count)

        self.logger.add_log(f"-1 RESULT: {item_data}")

    def press_export_all_csv(self):
        directory_path = self.get_dir_from_file_dialog(self.language.export_all)
        if not directory_path:
            return
        self.logger.add_log(f"EXPORT file scv to: {directory_path}")
        CSVExporter(item_datas=self.db_handler.retrieve_all_item_data(), path_dir=directory_path, is_backup=False)
        self.logger.add_log(f"EXPORT successful")
        self.open_done_window(self.language.export_all)

    def press_export_table_csv(self):
        directory_path = self.get_dir_from_file_dialog(self.language.export_current_table)
        if not directory_path:
            return
        self.logger.add_log(f"EXPORT file scv to: {directory_path} with filters :{str(self.filter_manager)}")
        CSVExporter(item_datas=self.db_handler.retrieve_item_data_with_filters(self.filter_manager), path_dir=directory_path, is_backup=False)
        self.logger.add_log(f"EXPORT successful")
        self.open_done_window(self.language.export_current_table)

    def press_settings(self):
        if self.window_setting is None:
            self.window_setting = SettingsWindow(main_window=self,
                                          appctxt=self.appctxt)
        self.window_setting.show()

    def press_logs(self):
        subprocess.Popen(f'explorer /select, "{os.getcwd()}\\log\\"', shell=True)

    def press_backup_now(self):
        CSVExporter(item_datas=self.db_handler.retrieve_all_item_data(), is_backup=True)
        self.logger.add_log(f"BACKUP")
        self.open_done_window(self.language.backup)

    def press_show_backup(self):
        subprocess.Popen(f'explorer /select, "{os.getcwd()}\\backup\\"', shell=True)

    def press_import_csv(self):
        # Handler for import CSV button press
        # Opens an ImportCSVWindow to import CSV data
        if self.window_import_csv is None:
            self.window_import_csv = ImportCSVWindow(main_window=self,
                                                     appctxt=self.appctxt,
                                                     db_handler=self.db_handler)
        self.window_import_csv.show()

    def open_done_window(self, title):
        if self.done_window is None:
            self.done_window = DoneWindow(self, self.appctxt, title)
        self.done_window.show()

    def update_group_name_comboBox(self):
        # Updates the group name ComboBox
        self.group_name_comboBox.clear()
        self.show_group_name_comboBox()

    def update_table(self):
        # Updates the table view with the latest data
        self.remove_rows()
        self.show_data_in_table()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.disable_btns()

    def update_language(self):
        self.in_stock_checkBox.setText(self.language.only_in_stock)
        self.edit_btn.setText(self.language.edit)
        self.copy_cod_btn.setText(self.language.cod)
        self.actionNew_items.setText(self.language.new_items)
        self.menuFile.setTitle(self.language.file)
        self.action_Settings.setText(self.language.settings)
        self.actionExport_All.setText(self.language.export_all)
        self.actionExport_current_table.setText(self.language.export_current_table)
        self.filters_label.setText(self.language.filters)


class ItemWindow(QWidget):
    def __init__(self, main_window: MainWindow, appctxt, db_handler, item_data=ItemData()):
        # Constructor for the ItemWindow class
        # Initializes the ItemWindow with the provided parameters
        # Loads the UI from a file using appctxt and sets up event connections
        super().__init__()
        loadUi(appctxt.get_resource("item.ui"), self)
        self.language = Language(Settings().language)
        self.setWindowTitle(self.language.item)
        self.logger = Logger()
        self.setStyleSheet(Theme(Settings().theme).get_theme())

        self.main_window = main_window
        self.db_handler = db_handler
        self.item_data = item_data

        self.init_buttons()
        self.init_group_comboBox()

        self.prev_version_data = None
        if not self.item_data.isNew():
            self.prev_version_data = self.item_data
            self.show_data()
        else:
            self.delete_btn.setEnabled(False)

        self.update_language()

    def init_buttons(self):
        self.cansel_btn.clicked.connect(self.press_cansel)
        self.save_btn.clicked.connect(self.press_save)
        self.delete_btn.clicked.connect(self.press_delete)

    def init_group_comboBox(self):
        # Initializes the group ComboBox and sets up event connection
        self.group_comboBox.currentIndexChanged.connect(self.on_combo_selection_change)
        self.add_group_names_to_comboBox()

    def press_save(self):
        # Handler for save button press
        # Extracts data from UI inputs, validates it, and either inserts or updates item data in the database
        self.change_item_data_from_inputs()
        if not self.item_data.isValid():
            return
        if self.item_data.isNew():
            self.insert_data_to_db()
            self.clear()
        else:
            self.change_data_in_db()
            self.close()

        self.main_window.update_table()
        self.main_window.update_group_name_comboBox()

    def insert_data_to_db(self):
        self.db_handler.insert_item_data(self.item_data)
        self.update_group_comboBox()
        self.logger.add_log(f"ADD: {self.item_data}")

    def change_data_in_db(self):
        self.db_handler.update_item_data(self.item_data)
        self.logger.add_log(f"UPDATE: {self.prev_version_data} UPDATE TO {self.item_data}")
        self.prev_version_data = self.item_data

    def clear(self):
        # Clears the UI input fields
        self.group_edit.setText("")
        self.taste_edit.setText("")
        self.nicotine_spinBox.setValue(0)
        self.volume_spinBox.setValue(0)
        self.price_doubleSpinBox.setValue(0)
        self.code_edit.setText("")
        self.count_spinBox.setValue(0)

    def change_item_data_from_inputs(self):
        self.item_data.setData(group_name=self.group_edit.text(),
                               taste=self.taste_edit.text(),
                               nicotine=self.nicotine_spinBox.value(),
                               volume=self.volume_spinBox.value(),
                               price=self.price_doubleSpinBox.value(),
                               code=self.code_edit.text(),
                               count=self.count_spinBox.value())

    def add_group_names_to_comboBox(self):
        # Populates the group ComboBox with group names from the database
        self.group_comboBox.addItem(self.language.select_group)
        for row in self.db_handler.retrieve_groups_names():
            self.group_comboBox.addItem(row[0])

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

    def on_combo_selection_change(self, index):
        # Handler for ComboBox selection change
        # Updates UI based on ComboBox selection
        if not self.group_comboBox.currentIndex() == 0:
            self.group_edit.setText(self.group_comboBox.currentText())
            self.group_comboBox.setCurrentIndex(0)

    def press_cansel(self):
        # Handler for cancel button press
        self.close()

    def press_delete(self):
        self.db_handler.delete_data_from_items(self.item_data.id_)
        self.logger.add_log(f"DELETE: {self.item_data}")
        self.main_window.update_table()
        self.main_window.update_group_name_comboBox()
        self.close()

    def update_group_comboBox(self):
        # Updates the group ComboBox content
        self.group_comboBox.clear()
        self.add_group_wwnames_to_comboBox()

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
        self.delete_btn.setText(self.language.delete)

    def closeEvent(self, event) -> None:
        self.main_window.window_item = None


class ImportCSVWindow(QWidget):
    def __init__(self, main_window: MainWindow, appctxt, db_handler):
        # Constructor for the ImportCSVWindow class
        # Initializes the window with the provided parameters
        # Loads the UI from a file using appctxt and sets up event connections
        super().__init__()
        loadUi(appctxt.get_resource("import_csv.ui"), self)
        self.appctxt = appctxt
        self.language = Language(Settings().language)
        self.logger = Logger()
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
        self.logger.add_log(f"Import file scv from: {self.path_edit.text()}")
        counter = 0
        for item_data in CSVImporter(self.path_edit.text()).get_in_item_data_list():
            if item_data.isValid():
                try:
                    self.db_handler.insert_item_data(item_data)
                    self.logger.add_log(f"ADD: {item_data}")
                    counter += 1
                except:
                    self.logger.add_log(f"ERROR ADD: {item_data}")
                    continue
        self.main_window.update_table()
        self.main_window.update_group_name_comboBox()
        self.main_window.open_done_window(f"{self.language.import_}: {counter}")
        self.close()

    def press_load_example(self):
        # Handler for load example button press
        # Allows users to load an example CSV file
        options = QFileDialog.Options()
        directory_dialog = QFileDialog()
        directory_path = directory_dialog.getExistingDirectory(self, 'Open Folder', '', options=options)
        if directory_path:
            shutil.copy(self.path_to_example, directory_path + '/' + self.path_to_example.split('\\')[-1])
            self.logger.add_log("Download example file scv")
        self.close()

    def update_language(self):
        self.load_example_btn.setText(self.language.load_example)
        self.browse_btn.setText(self.language.browse)

    def closeEvent(self, event) -> None:
        self.main_window.window_import_csv = None


class SettingsWindow(QDialog):
    def __init__(self, main_window: MainWindow, appctxt):
        super().__init__()
        loadUi(appctxt.get_resource("settings.ui"), self)
        self.language = Language(Settings().language)
        self.setWindowTitle(self.language.settings)
        self.logger = Logger()
        self.setStyleSheet(Theme(Settings().theme).get_theme())
        self.main_window = main_window


class DoneWindow(QDialog):
    def __init__(self, main_window:MainWindow, appctxt, name:str):
        super().__init__()
        loadUi(appctxt.get_resource("done.ui"), self)
        self.language = Language(Settings().language)
        self.setWindowTitle(name)
        self.logger = Logger()
        self.setStyleSheet(Theme(Settings().theme).get_theme())
        self.main_window = main_window

        self.close_btn.clicked.connect(self.close)

        self.update_language()

    def update_language(self):
        self.close_btn.setText(self.language.close)
        self.done_label.setText(self.language.done)

    def closeEvent(self, event) -> None:
        self.main_window.done_window = None


def main():
    db_handler = DatabaseHandler('database.db')
    db_handler.connect()
    db_handler.create_tables()

    appctxt = ApplicationContext()
    main_window = MainWindow(appctxt, db_handler)
    main_window.move(0, 0)
    main_window.setWindowTitle("Developed By @Valent_nk")
    main_window.show()
    try:
        sys.exit(appctxt.app.exec_())
    except ValueError as err:
        db_handler.close_connection()
        print("Exiting" + str(err))
