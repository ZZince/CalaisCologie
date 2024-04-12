from qtmodules import *

from textwrap import wrap


class GraphWidget(QWidget):
    """
    Widget designed to display graphs

    The graphs are rendered from an image file path.
    """

    def __init__(self, img_path: str = None):
        super().__init__()

        self._image_label = QLabel(self)
        self._image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._image_label.setScaledContents(True)
        self._image_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self._main_layout = QVBoxLayout()
        self._main_layout.addWidget(self._image_label)
        self.setLayout(self._main_layout)

        self._image_path = img_path

        self._image = QPixmap(self.size())
        self._image.fill(QColor(255, 255, 255))
        self._image_label.setPixmap(self._image)

        if self._image_path:
            self.load_image(self._image_path)

    def load_image(self, image_path: str):
        """
        Load an image from a file path

        :param image_path: path to the image file
        """
        self._image_path = image_path
        self._image.load(self._image_path)
        self._image_label.setPixmap(self._image)

    def load_text(self, text: str):
        """
        Load text in the widget

        :param text: text to display
        """
        # generate a pixmap from the text
        pixmap = QPixmap(self.size())
        pixmap.fill(QColor(255, 255, 255))

        painter = QPainter(pixmap)
        painter.setPen(QColor(0, 0, 0))
        # Use default font
        font = painter.font()
        font.setPointSize(20)
        painter.setFont(font)

        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter,
                         "\n".join(wrap(text, 25)))
        painter.end()

        self._image_label.setPixmap(pixmap)
