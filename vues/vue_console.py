
from qtmodules import *

import sys


class ConsoleWidget(QWidget):
    def __init__(self, default_text: str):
        super().__init__()

        self.text_edit = QTextEdit(default_text)
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet(
            "background-color:black; color:white; font-family: 'Fira Code', 'Consolas', monospace; font-size:12pt;")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text_edit)
        self.setLayout(self.layout)

    def write(self, message):
        self.text_edit.insertPlainText(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    console = ConsoleWidget('Hello\n')
    console.write('Hello, world!\n')

    sys.exit(app.exec())
