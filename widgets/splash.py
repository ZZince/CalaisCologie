import logging
import time
import typing
from qtmodules import *


class GradientTextWidget(QWidget):
    def __init__(self, text, parent=None, colors: list = None, fps: int = 60, animation_speed: int = 5):
        super().__init__(parent)
        self.text = text
        self.font_size = 24
        self.gradient = QLinearGradient(
            self.rect().topLeft().toPointF(), self.rect().bottomRight().toPointF()
        )

        if colors is None:
            colors = ["#0c1a33", "#60ff9b", "#0c1a33"]

        colors += colors[::-1]

        colors = [QColor(color) for color in colors]

        for i, color in enumerate(colors):
            self.gradient.setColorAt(i / len(colors), color)

        # Resize self to fit the text

        self.resize(self.font_size * len(self.text), self.font_size * 2)

        self.fps = fps
        self.animation_speed = animation_speed

        INTERVAL = int(1000 / self.fps)

        self.timer = QTimer(self)
        self.timer.setInterval(INTERVAL)
        self.timer.timeout.connect(self.update)

    def paintEvent(self, event):
        self.move_gradient()

        gradient = self.gradient
        rect = self.rect()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Gradient text
        font = painter.font()
        font.setPointSize(self.font_size)
        painter.setFont(font)
        painter.setPen(QPen(gradient, 0))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text)

    def move_gradient(self):

        # moves the gradient to the left and restarts it at the right
        self.gradient.setStart(
            QPointF(self.gradient.start().x() - self.animation_speed, 0))
        self.gradient.setFinalStop(
            QPointF(self.gradient.finalStop().x() - self.animation_speed, 0))

        if self.gradient.start().x() <= -self.width():
            # if self.gradient.start().x() <= 0:
            self.gradient.setStart(QPointF(self.width(), 0))
            self.gradient.setFinalStop(QPointF(self.width() * 2, 0))

    def start_animation(self):

        self.gradient.setStart(QPointF(0, 0))
        self.gradient.setFinalStop(QPointF(self.width(), self.height()))
        self.timer.start()

    def stop_animation(self):
        self.timer.stop()

    def setText(self, text):
        self.text = text
        self.resize(self.font_size * len(self.text), self.parent().height())
        self.move(self.parent().rect().center().x() - int(self.width() / 2),
                  self.parent().rect().center().y() - int(self.height() / 2))
        self.update()


class SplashScreen(QSplashScreen):
    def __init__(self, text, *args, **kwargs):
        """Show a splash screen for the given duration in ms"""

        # super().__init__(QPixmap("./interface/img/logo_Ccorp.png"))

        super().__init__(QPixmap("img/loading_background.png"))
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        # Make the splash screen not closable with a click
        self.setEnabled(False)

        # Show the GradientTextWidget
        self.gradient_text_widget = GradientTextWidget(
            text, self, *args, **kwargs)
        self.gradient_text_widget.setParent(self)

        self.gradient_text_widget.show()
        self.showMessage(text)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.close)

    def destroy_in(self, duration):
        logging.debug("SplashScreen: destroy_in" + str(duration))
        self.timer.start(duration)

    def showMessage(self, message: str, animated=False):
        self.gradient_text_widget.stop_animation()
        self.gradient_text_widget.setText(message)
        if animated:
            self.gradient_text_widget.start_animation()

        super().showMessage("", Qt.AlignmentFlag.AlignBottom)

    def block_thread_for(self, duration, start_animation=False):
        """Animate for the given duration in ms, blocking the main thread"""
        start = time.time()
        duration = duration / 1000

        if start_animation:
            self.gradient_text_widget.start_animation()

        while True:
            QApplication.processEvents()
            if time.time() - start > duration:
                break

    def block_for(self, duration):
        start = time.time()
        duration = duration / 1000
        while True:
            QApplication.processEvents()
            if time.time() - start > duration:
                break


if __name__ == "__main__":
    app = QApplication([])
    splash = SplashScreen(
        text="Chargement en cours...")
    splash.show()

    splash.destroy_in(5000)

    app.exec()
