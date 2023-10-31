import csv
from pathlib import Path
from typing import Dict, Union
from datetime import datetime

from setting import Settings


class FilterManager:
    def __init__(self, in_stock=True, group_name=None, search_teste=None):
        """Initialize a FilterManager instance.

        Args:
            in_stock (bool, optional): In-stock status filter. Defaults to True.
            group_name (str, optional): Group name filter. Defaults to None.
        """
        self.in_stock = in_stock
        self.group_name = group_name
        self.search_taste = search_teste

    def __str__(self):
        """Return a string representation of the FilterManager instance."""
        return f"FilterManager(in_stock={self.in_stock}, group_name={self.group_name}, search_taste={self.search_taste})"

    def to_tuple(self) -> Dict[str, Union[bool, str]]:
        """Convert FilterManager instance to a dictionary.

        Returns:
            Dict[str, Union[bool, str]]: Dictionary representation of the FilterManager instance.
        """
        return {'in_stock': self.in_stock, 'group_name': self.group_name, 'search_taste': self.search_taste}


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
    def __init__(self, path_file):
        """Initialize a CSVImporter instance.

        Args:
            path (str): Path to the CSV file.
        """
        self.path_file = path_file

    def get_in_list(self):
        """Read and return CSV data as a list.

        Returns:
            List[List[str]]: CSV data as a list of lists.
        """
        result = []
        with open(self.path_file, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                result.append(row)
        return result

    def get_in_item_data_list(self):
        """Convert CSV data to a list of ItemData instances.

            Args:
                path_to_csv (str): Path to the CSV file.

            Returns:
                List[List[ItemData]]: List of ItemData instances.
            """
        csv_in_list = self.get_in_list()
        if len(csv_in_list) == 1 or not csv_in_list:
            return []
        csv_in_list.pop(0)
        if len(csv_in_list[0]) < 7:
            return []
        return [ItemData(None, row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in csv_in_list]


class CSVExporter:
    def __init__(self, item_datas, path_dir=None, is_backup=False):
        self.item_datas = item_datas

        if is_backup:
            Path("backup").mkdir(parents=True, exist_ok=True)
            self.path_file = Path(f'backup/{datetime.now().strftime(Settings().format_data)}.csv')
            self.path_file.touch(exist_ok=True)
        else:
            self.path_file = Path(f"{path_dir}/{datetime.now().strftime(Settings().format_data)}.csv")
            self.path_file.touch()
        self.export_to_file()

    def export_to_file(self):
        with open(self.path_file, 'w', newline='', encoding='utf-8') as csv_file:

            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Group Name STRING',
                                 'Taste STRING',
                                 'Nicotine ml INTEGER',
                                 'Volume mg INTEGER',
                                 'Price FLOAT',
                                 'Code UNIQUE STRING',
                                 'Count INTEGER',
                                 'id'])
            # Write the data to the CSV file
            for itemData in self.item_datas:
                row = itemData.to_list()[1::]
                row.append(itemData.id_)
                csv_writer.writerow(row)
