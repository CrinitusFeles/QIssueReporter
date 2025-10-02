import asyncio
from pathlib import Path
import signal
from PyQt6 import QtWidgets
from PyQt6.uic.load_ui import loadUi
from qissuereporter.models import IssueContentModel
from qissuereporter.viewer.viewer_content import ContentWidget


class Viewer(QtWidgets.QWidget):
    tab_widget: QtWidgets.QTabWidget
    opened_issues_vlayout: QtWidgets.QVBoxLayout
    closed_issues_vlayout: QtWidgets.QVBoxLayout
    def __init__(self):
        super().__init__()
        loadUi(Path(__file__).parent / 'viewer.ui', self)
        self.widgets: list[ContentWidget] = []
        policy = QtWidgets.QSizePolicy.Policy.Expanding
        self.spacers: list[QtWidgets.QSpacerItem] = [
            QtWidgets.QSpacerItem(1, 1, vPolicy=policy),
            QtWidgets.QSpacerItem(1, 1, vPolicy=policy)
        ]
        self.opened_issues_vlayout.addItem(self.spacers[0])
        self.closed_issues_vlayout.addItem(self.spacers[1])

    def update_issues(self, issues: list[IssueContentModel]):
        self.opened_issues_vlayout.removeItem(self.spacers[0])
        self.closed_issues_vlayout.removeItem(self.spacers[1])
        for widget in self.widgets:
            widget.deleteLater()
        self.widgets.clear()
        opened_amount = 0
        closed_amount = 0
        for issue in issues:
            issue_widget = ContentWidget(issue)
            self.widgets.append(issue_widget)
            if issue.is_opened:
                opened_amount += 1
                self.opened_issues_vlayout.addWidget(issue_widget)
            else:
                closed_amount += 1
                self.closed_issues_vlayout.addWidget(issue_widget)
            issue_widget.fold_button.click()
        tab_bar = self.tab_widget.tabBar()
        if tab_bar:
            tab_bar.setTabText(0, f'Open ({opened_amount})')
            tab_bar.setTabText(1, f'Closed ({closed_amount})')
        self.opened_issues_vlayout.addItem(self.spacers[0])
        self.closed_issues_vlayout.addItem(self.spacers[1])


if __name__ == '__main__':
    from qasync import QEventLoop
    app = QtWidgets.QApplication([])
    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)
    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)
    w: Viewer = Viewer()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    w.show()
    with event_loop:
        event_loop.run_until_complete(app_close_event.wait())