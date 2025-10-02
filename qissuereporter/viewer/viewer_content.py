import base64
from pathlib import Path
from qcustomwidgets import Button, ImageBox
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.uic.load_ui import loadUi
from qissuereporter.creator.report_widget import Screenshot
from qissuereporter.models import IssueContentModel
from qissuereporter.image_view.image_viewer import ImageViewer


class ContentWidget(QtWidgets.QWidget):
    text_browser: QtWidgets.QTextBrowser
    dt_label: QtWidgets.QLabel
    title_button: QtWidgets.QPushButton
    number_label: QtWidgets.QLabel
    images_layout: QtWidgets.QHBoxLayout
    horizontal_layout: QtWidgets.QHBoxLayout
    main_layout: QtWidgets.QVBoxLayout
    scroll_area: QtWidgets.QScrollArea

    def __init__(self, data: IssueContentModel) -> None:
        super().__init__()
        loadUi(Path(__file__).parent / 'viewer_content.ui', self)
        self.number_label.setText(f'#{data.number}')
        self.title_button.setText(f' {data.title}')
        version: str = data.content.split()[0]
        if not version.startswith('v'):
            version = ''
        else:
            version = f'({version})'
        if data.is_opened:
            self.dt_label.setText(f'opened {data.created_at} {version}')
        else:
            self.dt_label.setText(f'closed {data.closed_at} {version}')
            icon = QtGui.QIcon(':/svg/issue-closed')
            self.title_button.setIcon(icon)
        self.url: str = data.url
        self._images: list[str] = data.images
        self.images_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.issue_type = Button(data.issue_type)
        self.set_issue_type_style(data.issue_type)
        self.issue_type.clicked.connect(self.issue_clicked)
        self.issue_type.setMaximumWidth(100)
        self.horizontal_layout.insertWidget(0, self.issue_type)
        if len(data.content.split()) > 1:
            text: str = '\n'.join([line for line in data.content.split()[1:]])
            self.text_browser.setMarkdown(text)
        else:
            self.text_browser.setMarkdown(data.content)
        self.fold_button = Button('', [':/svg/arrow-up-small',
                                       ':/svg/arrow-down-small'],
                                  flat=True, iterate_icons=True)
        self.title_button.clicked.connect(self.fold_button.click)
        self.fold_button.clicked.connect(self.on_fold)
        self.horizontal_layout.addWidget(self.fold_button, 1)
        if not data.images:
            self.scroll_area.deleteLater()
        else:
            for img in data.images:
                raw_image: bytes = base64.b64decode(img)
                image: QtGui.QImage = QtGui.QImage.fromData(raw_image)
                image_box = Screenshot(image, False)
                self.images_layout.addWidget(image_box)

    def set_issue_type_style(self, issue_type: str):
        if issue_type == 'Bug':
            color = "#e5534b"
            background = "#352c33"
        elif issue_type == 'Feature':
            color = "#478be6"
            background = "#253142"
        else:
            color = "#c68f27"
            background = "#36342c"
        self.issue_type.styleDict['default']['color'] = color
        self.issue_type.styleDict['default']['background-color'] = background
        self.issue_type.styleDict['hover']['color'] = color
        self.issue_type.styleDict['hover']['background-color'] = background
        self.issue_type.styleDict['press']['color'] = color
        self.issue_type.styleDict['press']['background-color'] = background

    def on_fold(self):
        state = self.text_browser.isHidden()
        if state:
            self.text_browser.show()
            if self._images:
                self.scroll_area.show()
        else:
            self.text_browser.hide()
            if self._images:
                self.scroll_area.hide()


    def issue_clicked(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.url))
