from qtmodules import *
import sys
from vues import MapWidget, ConsoleWidget
from widgets import CountrySelect, GraphWidget


class WorldView(QWidget):
    country_selected = pyqtSignal(str)
    airport_selected = pyqtSignal(float, float)

    def __init__(self):
        super().__init__()

        self.map_widget = MapWidget()
        self.map_widget.marker_clicked.connect(self.airport_selected)

        self.graph_widget = GraphWidget()
        self.graph_widget.setMaximumSize(500, 500)
        self.graph_widget.load_text(
            "Veuillez sélectionner un pays dans la liste ci-dessus.")

        self.country_select = CountrySelect()

        self.mainlayout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.mainlayout.addLayout(self.left_layout)
        self.mainlayout.addLayout(self.right_layout)

        self.left_layout.addWidget(self.map_widget)
        self.right_layout.addWidget(self.country_select)
        self.right_layout.addWidget(
            self.graph_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        self.country_select.item_selected.connect(self.changed_country)

        self.setLayout(self.mainlayout)

    def changed_country(self, country):
        self.country_selected.emit(country)


if __name__ == '__main__':
    app: QApplication = QApplication(sys.argv)
    w0: WorldView = WorldView()

    w0.show()

    sys.exit(app.exec())
