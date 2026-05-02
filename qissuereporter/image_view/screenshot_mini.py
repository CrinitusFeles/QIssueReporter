import base64
from PyQt6 import QtWidgets, QtGui, QtCore
from qcustomwidgets import Button, ImageBox

from qissuereporter.image_view.image_viewer import ImageViewer


def compress(image: QtGui.QImage, queality: int = 70) -> bytes:
    scaled: QtGui.QImage = image.scaled(
        int(image.width() * queality / 100),
        int(image.width() * queality / 100),
        QtCore.Qt.AspectRatioMode.KeepAspectRatio,
        QtCore.Qt.TransformationMode.FastTransformation
    )
    byte_array = QtCore.QByteArray()
    buffer = QtCore.QBuffer(byte_array)
    buffer.open(QtCore.QIODevice.OpenModeFlag.WriteOnly)
    scaled.save(buffer, 'PNG')
    return buffer.data()  # type: ignore

class Screenshot(Button):
    about_to_close = QtCore.pyqtSignal(QtWidgets.QWidget)
    def __init__(self, image: QtGui.QImage, closable: bool = True) -> None:
        super().__init__('', [ImageBox(image)], flat=False)
        self.source: QtGui.QImage = image
        self.image_view = ImageViewer(self.source)
        self.image = ImageBox(image)
        self.imageb64: str = base64.b64encode(compress(self.source, 80)).decode()
        self.setFixedHeight(90)
        self.setMinimumWidth(90)
        if closable:
            self.close_btn = Button('', [':/svg/close'], self, True)
            self.close_btn.clicked.connect(self.close_button_clicked)
            self.close_btn.move(5, 5)
        self.styleDict['default']['border-radius'] = 0
        self.styleDict['hover']['border-radius'] = 0
        self.styleDict['press']['border-radius'] = 0
        self.clicked.connect(self.image_view.show)

    def close_button_clicked(self):
        self.about_to_close.emit(self)
        self.deleteLater()

    def recompress(self, quality: int):
        self.imageb64 = base64.b64encode(compress(self.source, quality)).decode()
