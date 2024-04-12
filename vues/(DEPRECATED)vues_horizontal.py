
from qtmodules import *
import sys
#include <QAbstractItemView>

class HorizontalBar(QWidget):

    # datachanged = pyqtSignal(dict)
    clicked_confirm = pyqtSignal(dict)
    clicked_dowload = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.type_avion = QComboBox()
        self.type_avion.setFixedSize(250, 50)
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.addItem("Type d'avion")
        self.type_avion.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.type_avion.setStyleSheet("QComboBox {background-color: #2C92D5; color: #000000; border: 1px solid #000000; border-radius: 5px;}")
        self.type_avion.scroll(1, 1)
        
        self.pays_a = QComboBox()
        self.pays_a.setFixedSize(250, 50)
        self.pays_a.addItem("Pays Départ")
        self.pays_a.setStyleSheet("QComboBox {background-color: #2C92D5; color: #000000; border: 1px solid #000000; border-radius: 5px;}")

        self.pays_b = QComboBox()
        self.pays_b.setFixedSize(250, 50)
        self.pays_b.addItem("Pays Arrivé")
        self.pays_b.setStyleSheet("QComboBox {background-color: #2C92D5; color: #000000; border: 1px solid #000000; border-radius: 5px;}")
        
        
        self.taux_remplissage = QTextEdit()
        self.taux_remplissage.setFixedSize(250, 50)
        self.taux_remplissage.setText("Taux de remplissage")
        self.taux_remplissage.setStyleSheet("QTextEdit {background-color: #10EEF9; color: #000000; border: 1px solid #000000; border-radius: 5px;}")
        
        self.nombre_passager_max = QTextEdit()
        self.nombre_passager_max.setFixedSize(250, 50)
        self.nombre_passager_max.setText("Nombre de passager max")
        self.nombre_passager_max.setStyleSheet("QTextEdit {background-color: #10EEF9; color: #000000; border: 1px solid #000000; border-radius: 5px;}")

        
        self.consom_carburant = QTextEdit()
        self.consom_carburant.setFixedSize(250, 50)
        self.consom_carburant.setText("Consommation de carburant")
        self.consom_carburant.setStyleSheet("QTextEdit {background-color: #10EEF9; color: #000000; border: 1px solid #000000; border-radius: 5px;}")

        
        self.valider_data = QPushButton("Valider")
        self.valider_data.setFixedSize(250, 50)
        self.valider_data.setStyleSheet("QPushButton {background-color: #0E4C9F; color: #000000; border: 1px solid #000000; border-radius: 5px;}")
        
        self.download_data = QPushButton("Télécharger les données")
        self.download_data.setFixedSize(250, 50)
        self.download_data.setStyleSheet("QPushButton {background-color: #2C92D5; color: #000000; border: 1px solid #000000; border-radius: 5px;}")

        #self.logo_layout = QHBoxLayout()
        self.main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.middle_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.last_right_layout = QVBoxLayout()

        # self.typeAvion.setMinimumWidth(250)
        # self.paysA.setMinimumWidth(250)
        # self.paysB.setMinimumWidth(250)
        # self.tauxRemplissage.setMinimumWidth(250)
        # self.consomCarburant.setMinimumWidth(100)

        #self.logo_layout.addWidget(Photo())
        self.left_layout.addWidget(self.pays_a)
        self.left_layout.addWidget(self.type_avion)
        self.middle_layout.addWidget(self.pays_b)
        self.middle_layout.addWidget(self.taux_remplissage)
        self.right_layout.addWidget(self.nombre_passager_max)
        self.right_layout.addWidget(self.consom_carburant)
        self.last_right_layout.addWidget(self.valider_data)
        self.last_right_layout.addWidget(self.download_data)

        #self.main_layout.addLayout(self.logo_layout)
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.middle_layout)
        self.main_layout.addLayout(self.right_layout)
        self.main_layout.addLayout(self.last_right_layout)

        self.setLayout(self.main_layout)

        # self.typeAvion.currentIndexChanged.connect(self.update)
        # self.paysA.currentIndexChanged.connect(self.update)
        # self.paysB.currentIndexChanged.connect(self.update)
        # self.tauxRemplissage.textChanged.connect(self.update)
        # self.nombrePassagerMax.textChanged.connect(self.update)
        # self.consomCarburant.textChanged.connect(self.update)
        self.download_data.clicked.connect(self.download)
        self.valider_data.clicked.connect(self.valider)

    # def update(self):
    #    self.datachanged.emit(self.AllData())

    def valider(self):
        self.clicked_confirm.emit(self.get_inputs())

    def download(self):
        self.clicked_dowload.emit(self.get_inputs())

    def get_inputs(self):
        # Data queries
        data = {"typeavion": self.type_avion.currentIndex(),
                "paysA": self.pays_a.currentIndex(),
                "paysB": self.pays_b.currentIndex(),
                "tauxRemplissage": self.taux_remplissage.toPlainText(),
                "NombrePassager": self.nombre_passager_max.toPlainText(),
                "ConsomCarburant": self.consom_carburant.toPlainText(),
                }
        return data


if __name__ == '__main__':
    app: QApplication = QApplication(sys.argv)
    w0: HorizontalBar = HorizontalBar()

    w0.show()

    sys.exit(app.exec())
