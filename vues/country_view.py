from qtmodules import *
import sys
from vues import MapWidget, ConsoleWidget
from widgets import CountrySelect, GraphWidget


class CountryView(QWidget):
    country_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.country = QComboBox()
        self.country.view().setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.country.setStyleSheet(
            "QComboBox {background-color: #353534; border: none; padding: 5px; border-radius: 5px; font: bold 14px; min-width: 10em; padding: 6px; color: white;} background-color: #353534;")
        self.country.scroll(1, 1)
        self.country.setEditable(True)
        self.country.setCompleter(QCompleter(self.country.model()))
        self.country.isdropdown = True

        # ConsoleWidget à remplacer par des graphiques
        self.graph_widget1 = GraphWidget()
        self.graph_widget2 = GraphWidget()

        # 40% max screen size
        screen_size = QApplication.primaryScreen().size()
        max_graph_height = int(screen_size.height() * 0.5)
        self.graph_widget1.setMaximumHeight(max_graph_height)
        self.graph_widget2.setMaximumHeight(max_graph_height)

        # text instructions
        self.graph_widget1.load_text(
            "Veuillez sélectionner un pays pour afficher la part de vols intérieurs et internationaux")
        self.graph_widget2.load_text(
            "Veuillez sélectionner un pays pour afficher les 5 pays destination les plus courants")

        self.mainlayout = QVBoxLayout()
        self.toplayout = QHBoxLayout()
        self.bottomlayout = QHBoxLayout()

        self.country_select = CountrySelect()

        self.toplayout.addWidget(self.country_select)
        self.bottomlayout.addWidget(self.graph_widget1)
        self.bottomlayout.addWidget(self.graph_widget2)

        self.mainlayout.addLayout(self.toplayout)
        self.mainlayout.addLayout(self.bottomlayout)

        self.country_select.item_selected.connect(self.country_selected.emit)

        self.setLayout(self.mainlayout)

    # def changed_country(self, country):
    #     self.country_selected.emit(country)


if __name__ == '__main__':
    app: QApplication = QApplication(sys.argv)
    w0: CountryView = CountryView()

    w0.show()

    sys.exit(app.exec())
