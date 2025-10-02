from PyQt6 import QtWidgets, QtGui, QtCore


class CustomTextEdit(QtWidgets.QTextEdit):
    image_inserted = QtCore.pyqtSignal(QtGui.QImage)
    def insertFromMimeData(self, source):
        if source and source.hasUrls():
            for u in source.urls():
                if u.isLocalFile() and u.toLocalFile().endswith(('.jpg', '.png', '.tif', '.svg')):
                    self.image_inserted.emit(QtGui.QImage(u.toLocalFile()))
                else:
                    # If we hit a non-image or non-local URL break the loop and fall out
                    # to the super call & let Qt handle it
                    break
            else:
                # If all were valid images, finish here.
                return

        elif source and source.hasImage():
            data: QtGui.QImage = source.imageData()
            self.image_inserted.emit(data)
            return
        super().insertFromMimeData(source)
