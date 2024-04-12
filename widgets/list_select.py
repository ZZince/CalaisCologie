from qtmodules import *


class ListSelect(QWidget):
    """
    Widget permettant de sélectionner un item dans une liste déroulante.
    Utilisera une barre de recherche pour filtrer les aéroports.
    Utilisera une liste avec une scrollbar pour afficher les aéroports.
    """
    # TODO - Il faudra utiliser un QComboBox à l'extérieur pour sélectionner le pays.

    item_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.search_layout = QHBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Rechercher un élément")
        self.search_bar.textChanged.connect(self.search)
        self.search_layout.addWidget(self.search_bar, 1)

        self.search_button = QPushButton("🔎")
        self.search_button.clicked.connect(self.search)
        self.search_layout.addWidget(self.search_button, 0)

        self.layout.addLayout(self.search_layout)

        self.list_widget = QListWidget()
        self.list_widget.currentItemChanged.connect(
            lambda idx: self.select_list(idx) if idx else None)

        # Scrollbar
        self.list_widget.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.list_widget.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.layout.addWidget(self.list_widget)

        self.items = []

    def search(self):
        """
        Filtrer les aéroports en fonction de la recherche.
        """
        self.list_widget.setCurrentIndex(-1)
        search_text = self.search_bar.text()
        self.list_widget.clear()
        for airport in self.items:
            if search_text.lower() in airport.lower():
                self.list_widget.addItem(airport)

    def select_list(self, item):
        """
        Émettre un signal avec l'item sélectionné.
        """
        self.item_selected.emit(item.text())

    def set_list(self, items: list[str]):
        """
        Définir la liste des items.
        """
        self.items = items
        self.search()
