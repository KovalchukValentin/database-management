import csv
from typing import Dict, Union


class Settings:
    def __init__(self):
        self.language = "ua"
        self.theme = "dark_gray"


class Theme:
    def __init__(self, theme="dark_gray"):
        self.theme = theme

    def get_theme(self) -> str:
        if self.theme == "dark_gray":
            return """
                QWidget{
                    background-color: #333333;
                }
                QSpinBox {
                    background-color: #333333;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    border-radius: 4px;
                    padding: 2px; /* Adjust the padding as needed */
                }
                QDoubleSpinBox {
                    background-color: #333333;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    border-radius: 4px;
                    padding: 2px; /* Adjust the padding as needed */
                }
                QLineEdit {
                    background-color: #333333;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    border-radius: 4px;
                }
                QLineEdit:focus {
                    border: 1px solid #888888;
                }
                QMainWindow {
                    background-color: #333333;
                }
                QPushButton {
                    background-color: #555555;
                    color: #FFFFFF;
                    border: 1px solid #333333;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #777777;
                }
                QPushButton:disabled {
                    background-color: #555555;
                    color: #888888;
                    border: 1px solid #333333;
                    border-radius: 4px;
                }
                QTableView {
                    background-color: #333333;
                    color: #FFFFFF;
                    gridline-color: #555555;
                    border: 1px solid #555555;
                }
                QHeaderView {
                    background-color: #555555;
                }
                QHeaderView::section {
                    background-color: #555555;
                    color: #FFFFFF;
                    border: 1px solid #333333;
                }
                QLabel {
                    color: #FFFFFF;
                }
                QComboBox {
                    background-color: #333333;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    border-radius: 4px;
                    padding: 2px; /* Adjust the padding as needed */
                }
                QComboBox QAbstractItemView {
                    background-color: #333333;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                }
                QCheckBox {
                    color: #FFFFFF;
                }
                QVBoxLayout, QHBoxLayout {
                    background-color: #333333;
                    border: 1px solid #555555;
                }
                QDialog {
                    background-color: #333333;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                }
                QScrollArea {
                    background-color: #333333;
                }
                QScrollBar:vertical, QScrollBar:horizontal {
                    background-color: #333333;
                }
                QScrollBar:vertical {
                    width: 12px;
                }
                QScrollBar:horizontal {
                    height: 12px;
                }
                QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                    background-color: #555555;
                    border: 1px solid #333333;
                    border-radius: 6px;
                }
                QScrollBar::add-line, QScrollBar::sub-line, QScrollBar::add-page, QScrollBar::sub-page {
                    background-color: #333333;
                    border: 1px solid #555555;
                    border-radius: 4px;
                }
            """
        if self.theme == "dark":
            return ""
        if self.theme == 'light':
            return ""



class Language:
    def __init__(self, language: str):
        self.language = language
        self.init_language()
        self.update()

    def init_language(self) -> None:
        self.all = "All"
        self.only_in_stock = "Only in stock"
        self.confirm = "Confirm"
        self.save = "Save"
        self.cansel = "Cansel"
        self.group = "Group"
        self.taste = "Taste"
        self.volume = "Volume"
        self.count = "Count"
        self.price = "Price"
        self.cod = "Cod"
        self.nicotine = "Nicotine"
        self.add_items = "Add items"
        self.edit = "Edit"
        self.item = "Item"
        self.select_group = "Select group"
        self.load_example = "Load example"
        self.browse = "Browse"

    def setLanguage(self, language: str) -> None:
        self.language = language
        self.update()

    def update(self) -> None:
        if self.language.lower() == "ua":
            self.all = "Всі"
            self.only_in_stock = "Тільки в наявності"
            self.confirm = "Підтвертити"
            self.save = "Зберегти"
            self.cansel = "Відмінити"
            self.group = "Група"
            self.taste = "Смак"
            self.volume = "Об'єм"
            self.count = "Кількість"
            self.price = "Ціна"
            self.cod = "Код"
            self.nicotine = "Нікотин"
            self.add_items = "Додати"
            self.edit = "Редагувати"
            self.item = "Елемент"
            self.select_group = "Обрати групу"
            self.load_example = "Завантажити приклад"
            self.browse = "Знайти"
        else:
            self.init_language()


class FilterManager:
    def __init__(self, in_stock=True, group_name=None):
        """Initialize a FilterManager instance.

        Args:
            in_stock (bool, optional): In-stock status filter. Defaults to True.
            group_name (str, optional): Group name filter. Defaults to None.
        """
        self.in_stock = in_stock
        self.group_name = group_name

    def __str__(self):
        """Return a string representation of the FilterManager instance."""
        return f"FilterManager(in_stock={self.in_stock}, group_name={self.group_name})"

    def to_tuple(self) -> Dict[str, Union[bool, str]]:
        """Convert FilterManager instance to a dictionary.

        Returns:
            Dict[str, Union[bool, str]]: Dictionary representation of the FilterManager instance.
        """
        return {'in_stock': self.in_stock, 'group_name': self.group_name}


class ItemData:
    def __init__(self, id_=None, group_name=None, taste=None, nicotine=None, volume=None, price=None, code=None,
                 count=None):
        """Initialize an ItemData instance.

        Args:
            id_ (str, optional): ID of the item. Defaults to None.
            group_name (str, optional): Group name of the item. Defaults to None.
            taste (str, optional): Taste of the item. Defaults to None.
            nicotine (int, optional): Nicotine content of the item. Defaults to None.
            volume (int, optional): Volume of the item. Defaults to None.
            price (float, optional): Price of the item. Defaults to None.
            code (str, optional): Code of the item. Defaults to None.
            count (int, optional): Count of the item. Defaults to None.
        """
        self.id_ = id_
        self.group_name = group_name
        self.taste = taste
        self.nicotine = nicotine
        self.volume = volume
        self.price = price
        self.code = str(code)
        self.count = count

    def setData(self, group_name=None, taste=None, nicotine=None, volume=None, price=None, code=None, count=None):
        """Set data for the item.

        Args:
            group_name (str, optional): Group name of the item. Defaults to None.
            taste (str, optional): Taste of the item. Defaults to None.
            nicotine (int, optional): Nicotine content of the item. Defaults to None.
            volume (int, optional): Volume of the item. Defaults to None.
            price (float, optional): Price of the item. Defaults to None.
            code (str, optional): Code of the item. Defaults to None.
            count (int, optional): Count of the item. Defaults to None.
        """
        self.group_name = group_name
        self.taste = taste
        self.nicotine = nicotine
        self.volume = volume
        self.price = price
        self.code = str(code)
        self.count = count

    def isValid(self) -> bool:
        """Check if the item data is valid.

        Returns:
            bool: True if the item data is valid, False otherwise.
        """
        if None in (self.group_name, self.taste, self.nicotine, self.volume, self.price, self.code, self.count):
            return False
        return True

    def isNew(self) -> bool:
        """Check if the item is new.

        Returns:
            bool: True if the item is new, False otherwise.
        """
        return self.id_ is None

    def __str__(self):
        """Return a string representation of the ItemData instance."""
        return f"ItemData(id={self.id_}, group_name={self.group_name}, taste={self.taste}, " \
               f"nicotine={self.nicotine}, volume={self.volume}, price={self.price}, " \
               f"code={self.code}, count={self.count})"

    def to_list(self):
        """Convert ItemData instance to a list.

        Returns:
            List: List representation of the ItemData instance.
        """
        return [self.id_, self.group_name, self.taste, self.nicotine, self.volume, self.price, self.code, self.count]


class CSVImporter:
    def __init__(self, path):
        """Initialize a CSVImporter instance.

        Args:
            path (str): Path to the CSV file.
        """
        self.path = path

    def get_in_list(self):
        """Read and return CSV data as a list.

        Returns:
            List[List[str]]: CSV data as a list of lists.
        """
        result = []
        with open(self.path, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                result.append(row)
        return result


def path_csv_to_items_data(path_to_csv: str):
    """Convert CSV data to a list of ItemData instances.

    Args:
        path_to_csv (str): Path to the CSV file.

    Returns:
        List[List[ItemData]]: List of ItemData instances.
    """
    csv_in_list = CSVImporter(path_to_csv).get_in_list()
    if len(csv_in_list) == 1 or not csv_in_list:
        return []
    csv_in_list.pop(0)
    if len(csv_in_list[0]) < 7:
        return []
    return [ItemData(None, row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in csv_in_list]