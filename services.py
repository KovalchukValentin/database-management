class ItemData:
    def __init__(self, id_=None, group_name=None, taste=None, nicotine=None, volume=None, price=None, code=None, count=None):
        self.id_ = id_
        self.group_name = group_name
        self.taste = taste
        self.nicotine = nicotine
        self.volume = volume
        self.price = price
        self.code = code
        self.count = count

    def isValid(self) -> bool:
        if None in (self.group_name, self.taste, self.nicotine, self.volume, self.price, self.code, self.count):
            return False
        return True

    def isNew(self) -> bool:
        return self.id_ is not None
