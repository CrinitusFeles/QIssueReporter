from PyQt6 import QtWidgets, QtGui, QtCore
from qcustomwindow import CustomWindow


class ImageViewer(CustomWindow):
    def __init__(self, image: QtGui.QImage) -> None:
        super().__init__()
        self.label = QtWidgets.QLabel(self)
        self.label.setScaledContents(True)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding,
                                 QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        self.pix = QtGui.QPixmap.fromImage(image)
        self.label.setPixmap(self.pix)
        self.addWidget(self.label)
        self.resize(image.size())

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        self.label.resize(self.body.size())
        pal: QtGui.QPalette = self.palette()
        arm =  QtCore.Qt.AspectRatioMode.KeepAspectRatioByExpanding
        tm = QtCore.Qt.TransformationMode.SmoothTransformation
        brush = QtGui.QBrush(self.pix.scaled(self.body.size(), arm, tm))
        pal.setBrush(self.backgroundRole(), brush)
        self.label.setPalette(pal)
