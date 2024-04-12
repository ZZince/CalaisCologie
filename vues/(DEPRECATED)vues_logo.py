from qtmodules import *
import sys
import os


class Photo(QWidget):
    def __init__(self, url=os.path.join(os.path.dirname(__file__), "logo.png")):
        super().__init__()
        self.pic = QLabel(self)
        self.pic.setPixmap(QPixmap(url))

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.pic)


if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    window = Photo()
    window.show()
    # start
    sys.exit(app.exec())
