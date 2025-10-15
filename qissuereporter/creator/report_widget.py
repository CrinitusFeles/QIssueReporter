from pathlib import Path
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.uic.load_ui import loadUi
from loguru import logger
from qissuereporter.models import BugReportModel
from qissuereporter.image_view.screenshot_mini import Screenshot
from qissuereporter.creator.text_edit import CustomTextEdit


class BugReport(QtWidgets.QWidget):
    report_button: QtWidgets.QPushButton
    compress_button: QtWidgets.QPushButton
    description_label_1: QtWidgets.QLabel
    description_label_2: QtWidgets.QLabel
    description_layout: QtWidgets.QVBoxLayout
    images_layout: QtWidgets.QVBoxLayout
    title_line_edit: QtWidgets.QLineEdit
    combo_box: QtWidgets.QComboBox
    editor_tabs: QtWidgets.QTabWidget
    markdown_preview: QtWidgets.QTextBrowser
    quality_spin_box: QtWidgets.QSpinBox
    size_label: QtWidgets.QLabel

    report_created = QtCore.pyqtSignal(BugReportModel)
    def __init__(self, version: str, username: str = '') -> None:
        super().__init__()
        loadUi(Path(__file__).parent / 'bug_report.ui', self)
        self.version: str = version
        self.username: str = username
        self.images_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.text_edit = CustomTextEdit()
        self.text_edit.setPlaceholderText('Please enter details or insert image')
        self.description_layout.addWidget(self.text_edit)
        self.text_edit.image_inserted.connect(self.on_image_inserted)
        self.editor_tabs.currentChanged.connect(self.on_tab_changed)
        self.images: list[Screenshot] = []

    def on_tab_changed(self):
        if self.editor_tabs.currentIndex() == 1:
            self.markdown_preview.setMarkdown(self.text_edit.toPlainText())

    def on_compress_button_pressed(self):
        full_size = 0
        if not self.images:
            return
        for image in self.images:
            image.recompress(self.quality_spin_box.value())
            full_size += len(image.imageb64) + 50
        full_size += len(self.text_edit.toPlainText())
        self.size_label.setText(f'{full_size}')
        if full_size > 0xFFFF:
            self.size_label.setStyleSheet('color: red;')
        else:
            self.size_label.setStyleSheet('color: palette(text);')

    def on_report_button_pressed(self):
        details: str = self.text_edit.toPlainText()
        title: str = self.title_line_edit.text()
        if not title:
            logger.warning('Title must not be empty')
            return
        if not details:
            logger.warning('Details must not be empty')
            return
        report_type: str = self.combo_box.currentText()
        images_b64: list[str] = [image.imageb64 for image in self.images]
        full_size = 0
        for image_data in images_b64:
            full_size += len(image_data)
        report = BugReportModel(report_type=report_type,
                                title=title,
                                details=details,
                                images=images_b64,
                                username=self.username,
                                version=self.version,
                                images_size=full_size,
                                client_version=self.version)
        self.report_created.emit(report)

    def refresh_widget(self):
        self.text_edit.clear()
        self.title_line_edit.clear()
        for widget in self.images:
            widget.deleteLater()
        self.images.clear()
        self.combo_box.setCurrentIndex(0)

    def on_image_inserted(self, image: QtGui.QImage):
        if self.images_layout.count() < 5:
            widget = Screenshot(image)
            widget.about_to_close.connect(self.image_deleted)
            self.images_layout.addWidget(widget)
            self.images.append(widget)
            self.on_compress_button_pressed()
        else:
            logger.warning('Maximum 5 screenshots')

    def image_deleted(self, image: Screenshot):
        self.images.remove(image)
        self.on_compress_button_pressed()