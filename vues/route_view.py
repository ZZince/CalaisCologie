from qtmodules import *
from vues import ConsoleWidget
import sys
from widgets import CountrySelect, BestRouteWidget
from vues import MapWidget


class RouteView(QWidget):

    # datachanged = pyqtSignal(dict)
    clicked_confirm = pyqtSignal(dict)
    clicked_dowload = pyqtSignal(str, str)

    country_choiced_left = pyqtSignal(str)
    country_choiced_right = pyqtSignal(str)

    aero_choiced = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        self.left_airport_selected = None
        self.right_airport_selected = None
        
        self.create_widgets()
        self.connect_widgets()

    def create_widgets(self):

        # Country selects
        self.country_select1 = CountrySelect()
        self.country_select2 = CountrySelect()

        # aero 1
        self.aero1 = QComboBox()
        self.aero1.view().setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.aero1.setStyleSheet(
            "QComboBox {background-color: #353534; border: none; padding: 5px; border-radius: 5px; font: bold 14px; min-width: 10em; padding: 6px; color: white;} background-color: #353534;")
        self.aero1.scroll(1, 1)
        self.aero1.setEditable(True)
        self.aero1.setCompleter(QCompleter(self.aero1.model()))
        self.aero1.isdropdown = True

        # aero 2
        self.aero2 = QComboBox()
        self.aero2.view().setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.aero2.setStyleSheet(
            "QComboBox {background-color: #353534; border: none; padding: 5px; border-radius: 5px; font: bold 14px; min-width: 10em; padding: 6px; color: white;} background-color: #353534;")
        self.aero2.scroll(1, 1)
        self.aero2.setEditable(True)
        self.aero2.setCompleter(QCompleter(self.aero2.model()))
        self.aero2.isdropdown = True

        # Central data widgets
        self.best_route_widget = BestRouteWidget()
        self.map_widget = MapWidget()

        self.download_button = QPushButton("Télécharger les données")
        self.download_button.setStyleSheet(
            " QPushButton {background-color: #353534;border-style: outset; border-width: 2px; border-radius: 10px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px; color: white; } QPushButton:pressed {background-color: #F0F8FF;} QPushButton:hover {border-color: lightblue;}")

        # Layouts
        self.master_layout = QVBoxLayout()
        self.main_layout = QHBoxLayout()
        self.bottom_layout = QHBoxLayout()

        self.left_layout = QVBoxLayout()

        self.left_layout.addWidget(self.country_select1)
        self.left_layout.addWidget(self.aero1)
        self.main_layout.addLayout(self.left_layout)

        self.middle_layout = QVBoxLayout()

        self.middle_layout.addWidget(self.best_route_widget)
        self.middle_layout.addWidget(self.map_widget)
        self.main_layout.addLayout(self.middle_layout, 2)

        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(self.country_select2)
        self.right_layout.addWidget(self.aero2)
        self.main_layout.addLayout(self.right_layout)

        self.setLayout(self.master_layout)

    def connect_widgets(self):
        self.master_layout.addLayout(self.main_layout)
        self.master_layout.addWidget(self.download_button)

        self.download_button.clicked.connect(self.download)
        self.country_select1.item_selected.connect(self.country_selected1)
        self.country_select2.item_selected.connect(self.country_selected2)
        self.aero1.currentIndexChanged.connect(
            lambda idx: self.aero_changed_left(
                self.aero1.currentText()) if idx != -1 else None
        )
        self.aero2.currentIndexChanged.connect(
            lambda idx: self.aero_changed_right(
                self.aero2.currentText()) if idx != -1 else None
        )

    def download(self):
        self.clicked_dowload.emit(self.left_airport_selected, self.right_airport_selected)

    def aero_changed_left(self, aero):
        self.left_airport_selected = aero
        print(aero)
        if self.left_airport_selected is not None and self.right_airport_selected is not None:
            self.aero_choiced.emit(aero, self.right_airport_selected)

    def aero_changed_right(self, aero):
        self.right_airport_selected = aero
        if self.left_airport_selected is not None and self.right_airport_selected is not None:
            self.aero_choiced.emit(self.left_airport_selected, aero)

    def country_selected1(self, country):
        self.country_choiced_left.emit(country)

    def country_selected2(self, country):
        self.country_choiced_right.emit(country)

    def update_leftcombobox(self, airports: list):
        self.aero1.clear()
        self.aero1.setCurrentIndex(-1)
        for airport in airports:
            self.aero1.addItem(airport)

    def update_rightcombobox(self, airports: list):
        self.aero2.clear()
        self.aero2.setCurrentIndex(-1)
        for airport in airports:
            self.aero2.addItem(airport)


if __name__ == '__main__':
    app: QApplication = QApplication(sys.argv)
    w0: RouteView = RouteView()
    w0.show()

    sys.exit(app.exec())
