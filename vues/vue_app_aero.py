from qtmodules import *
import sys
from vues import MapWidget, ConsoleWidget

class Aero(QWidget):
    def __init__(self):
        super().__init__()

        self.console = ConsoleWidget("Console Aero")
        self.console.setFixedSize(500, 600)
        self.mapav = MapWidget()
        
        self.download_data = QPushButton("Télécharger les données")
        self.download_data.setFixedSize(250, 50)
        self.download_data.setStyleSheet("QPushButton {background-color: #2C92D5; color: #000000; border: 1px solid #000000; border-radius: 5px; text-align: center;}")
        self.download_data.setStyleSheet(" QPushButton {background-color: #353534;border-style: outset; border-width: 2px; border-radius: 10px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px; color: white; } QPushButton:pressed {background-color: #F0F8FF;} QPushButton:hover {border-color: lightblue;}")

        self.mainlayout = QVBoxLayout()
        self.toplayout = QHBoxLayout()
        self.bottomlayout = QHBoxLayout()
        
        self.toplayout.addWidget(self.mapav)
        self.toplayout.addWidget(self.console)
        self.bottomlayout.addWidget(self.download_data)
        self.mainlayout.addLayout(self.toplayout)
        self.mainlayout.addLayout(self.bottomlayout)
        
        self.setLayout(self.mainlayout)

if __name__ == '__main__':
    app: QApplication = QApplication(sys.argv)
    w0: Aero = Aero()

    w0.show()

    sys.exit(app.exec())
