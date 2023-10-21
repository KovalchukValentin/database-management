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