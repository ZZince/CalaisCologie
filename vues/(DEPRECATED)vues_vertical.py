
from qtmodules import *
from .vue_console import ConsoleWidget

import sys


class VerticalBar(QLabel):
    def __init__(self):
        super().__init__()

        self.main_layout = QHBoxLayout()
        self.top_layout = QVBoxLayout()
        self.bottom_layout = QVBoxLayout()

        self.CO2_data = QLabel(
            "Voici les données récupérés sur le CO2 libéré")  # Per default values
        self.CO2_data.setStyleSheet("QLabel {background-color: #2C92D5; color: #000000; border: 1px ; border-radius: 10px; padding-bottom: 420px;}")
        self.various_data = QLabel(
            "Voici les données diverses affichées")
        self.various_data.setStyleSheet("QLabel {background-color: #2C92D5; color: #000000; border: 1px; border-radius: 10px; padding-bottom: 420px;}")


        # self.left_diagram = QLabel()  # Les QLabel sont nécessaires pour les QPixmap
        #self.left_diagram.setPixmap(
        #    QPixmap("logo_Ccorp.png"))  # Per default values
        #self.right_diagram = QLabel()
        #self.right_diagram.setPixmap(QPixmap("logo_Ccorp.png"))

        self.top_layout.addWidget(self.CO2_data)
        #self.top_layout.addWidget(self.left_diagram)
        self.bottom_layout.addWidget(self.various_data)
        #self.bottom_layout.addWidget(self.right_diagram)
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.bottom_layout)

        self.setLayout(self.main_layout)


if __name__ == '__main__':
    app: QApplication = QApplication(sys.argv)
    w0: VerticalBar = VerticalBar()

    w0.show()

    sys.exit(app.exec())
