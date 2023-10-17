import csv
from typing import Dict, Union


class FilterManager:
    def __init__(self, in_stock=True, group_name=None):
        self.in_stock = in_stock
        self.group_name = group_name

    def __str__(self):
        return f"FilterManager(in_stock={self.in_stock}, group_name={self.group_name})"

    def to_tuple(self) -> Dict[str, Union[bool, str]]:
        return {'in_stock': self.in_stock, 'group_name': self.group_name}


class ItemData:
    def __init__(self, id_=None, group_name=None, taste=None, nicotine=None, volume=None, price=None, code=None,
                 count=None):
        self.id_ = id_
        self.group_name = group_name
        self.taste = taste
        self.nicotine = nicotine
        self.volume = volume
        self.price = price
        self.code = str(code)
        self.count = count

    def setData(self, group_name=None, taste=None, nicotine=None, volume=None, price=None, code=None, count=None):
        self.group_name = group_name
        self.taste = taste
        self.nicotine = nicotine
        self.volume = volume
        self.price = price
        self.code = str(code)
        self.count = count

    def isValid(self) -> bool:
        if None in (self.group_name, self.taste, self.nicotine, self.volume, self.price, self.code, self.count):
            return False
        return True

    def isNew(self) -> bool:
        return self.id_ is None

    def __str__(self):
        return f"ItemData(id={self.id_}, group_name={self.group_name}, taste={self.taste}, " \
               f"nicotine={self.nicotine}, volume={self.volume}, price={self.price}, " \
               f"code={self.code}, count={self.count})"

    def to_list(self):
        return [self.id_, self.group_name, self.taste, self.nicotine, self.volume, self.price, self.code, self.count]


class CSVImporter:
    def __init__(self, path):
        self.path = path

    def get_in_list(self):
        result = []
        with open(self.path, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                result.append(row)
        return result


def path_csv_to_items_data(path_to_csv: str):
    csv_in_list = CSVImporter(path_to_csv).get_in_list()
    if len(csv_in_list) == 1 or not csv_in_list:
        return []
    csv_in_list.pop(0)
    if len(csv_in_list[0]) < 7:
        return []
    return [ItemData(None, row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in csv_in_list]