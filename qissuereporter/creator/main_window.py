import asyncio
from PyQt6 import QtWidgets, QtCore
import qasync
from qcustomwindow import CustomWindow
import signal
from qissuereporter.creator.report_widget import BugReport
from qissuereporter.models import BugReportModel
from qissuereporter.api import create_issue
from qissuereporter import __version__


class ReporterWindow(CustomWindow):
    report_created = QtCore.pyqtSignal(BugReportModel)
    def __init__(self, version: str, url: str, token: str) -> None:
        super().__init__()
        self.url: str = url
        self.token: str = token
        self.widget = BugReport(version)
        self.setTitle('Issue Reporter')
        self.widget.report_created.connect(self.on_report_created)
        self.body_layout.addWidget(self.widget)

    @qasync.asyncSlot(BugReportModel)
    async def on_report_created(self, report: BugReportModel) -> None:
        result: bool = await create_issue(self.url, self.token, report.query())
        if result:
            self.widget.refresh_widget()
            self.report_created.emit(report)


if __name__ == '__main__':
    from qasync import QEventLoop
    app = QtWidgets.QApplication([])
    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)
    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)
    w: ReporterWindow = ReporterWindow(__version__, '', '')
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    w.show()
    with event_loop:
        event_loop.run_until_complete(app_close_event.wait())
