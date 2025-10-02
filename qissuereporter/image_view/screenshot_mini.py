import base64
from PyQt6 import QtWidgets, QtGui, QtCore
from qcustomwidgets import Button, ImageBox
import io
from PIL import ImageQt

from qissuereporter.image_view.image_viewer import ImageViewer


def compress(image: QtGui.QImage, queality: int = 70) -> bytes:
    buffered = io.BytesIO()
    img = ImageQt.fromqimage(image).convert('RGB')
    img.save(buffered, optimize=True, format="JPEG", quality=queality)
    return buffered.getvalue()


class Screenshot(Button):
    about_to_close = QtCore.pyqtSignal(QtWidgets.QWidget)
    def __init__(self, image: QtGui.QImage, closable: bool = True) -> None:
        super().__init__('', [ImageBox(image)], flat=False,
                         full_size_image=True, side_margins=0)
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
