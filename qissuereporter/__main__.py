
import asyncio
import signal
from PyQt6 import QtWidgets
from qissuereporter.creator.main_window import ReporterWindow
from qissuereporter.viewer.main_window import ViewerWindow


token = ''
url = ''


if __name__ == '__main__':
    from qasync import QEventLoop
    from qcustomwidgets import dark, stylesheet
    app = QtWidgets.QApplication([])
    app.setStyleSheet(stylesheet)
    dark()
    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)
    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)
    viewer: ViewerWindow = ViewerWindow(url, token)
    reporter: ReporterWindow = ReporterWindow(url, token)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    viewer.show()
    reporter.show()
    with event_loop:
        event_loop.run_until_complete(app_close_event.wait())
