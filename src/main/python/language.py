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
        self.delete = "Delete"
        self.file = "File"
        self.settings = "Settings"
        self.new_items = "New items"
        self.export_all = "Export all"
        self.export_current_table = "Export current table"

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
            self.delete = "Видалити"
            self.file = "Файл"
            self.settings = "Налатування"
            self.new_items = "Додати нові"
            self.export_all = "Експортувати все"
            self.export_current_table = "Експорт поточної таблиці"
        else:
            self.init_language()