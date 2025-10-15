import asyncio
from pydantic import ValidationError
import qasync
import signal
from qcustomwindow import CustomWindow
from PyQt6 import QtWidgets, QtCore
from qcustomwidgets import Button
from qcustomwidgets.widgets.spinner import Spinner
from qissuereporter.viewer.viewer import Viewer
from qissuereporter.models import BugReportModel, ContentJSON, IssueContentModel
from qissuereporter.api import calc_delta, get_issues


image_str = '<img src="data:image/jpeg;base64,'


class ViewerWindow(CustomWindow):
    report_created = QtCore.pyqtSignal(BugReportModel)
    def __init__(self, url: str, token: str) -> None:
        super().__init__()
        self.widget = Viewer()
        self.url: str = url
        self.token: str = token
        self.setTitle('Issue Viewer')
        self.body_layout.addWidget(self.widget)
        self.timer = QtCore.QTimer()
        self.timer.singleShot(0, self.startup)
        self.spinner = Spinner(4, 'green')
        self.spinner.setFixedSize(20, 20)
        self.update_button = Button('Refresh', [':/svg/update'], self)
        self.update_button.clicked.connect(self._request_issues)
        self.update_button.body_layot.addWidget(self.spinner)
        self.add_left_widget(self.update_button)

    def startup(self):
        asyncio.create_task(self.request_issues())

    @qasync.asyncSlot()
    async def _request_issues(self):
        await self.request_issues()

    async def request_issues(self):
        self.spinner.setVisible(True)
        answer: list[dict] = await get_issues(self.url, self.token)
        self.spinner.setVisible(False)
        if answer:
            models: list[IssueContentModel] = []
            for issue in answer:
                try:
                    content_json: ContentJSON = ContentJSON.model_validate_json(issue['body'])
                    images = [image[len(image_str):-17] for image in content_json.images]
                    content = content_json.content
                    username = content_json.username
                    version = content_json.version
                except ValidationError as err:
                    images = []
                    content = issue['body']
                    username = ''
                    version = ''
                created_at: str = calc_delta(issue['created_at'])
                if issue['closed_at']:
                    closed_at: str = calc_delta(issue['closed_at'])
                else:
                    closed_at = issue['closed_at']
                issue_type = issue['type']
                if issue_type is None:
                    issue_name: str = 'Bug'
                else:
                    issue_name = issue_type['name']
                model = IssueContentModel(images=images,
                                          number=issue['number'],
                                          url=issue['html_url'],
                                          is_opened=(issue['state'] == 'open'),
                                          title=issue['title'],
                                          version=version,
                                          username=username,
                                          content=content,
                                          created_at=created_at,
                                          issue_type=issue_name,
                                          closed_at=closed_at,
                                          close_reason=issue['state_reason'])
                models.append(model)
            self.widget.update_issues(models)


if __name__ == '__main__':
    from qasync import QEventLoop
    app = QtWidgets.QApplication([])
    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)
    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)
    w: ViewerWindow = ViewerWindow('', '')
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    w.show()
    with event_loop:
        event_loop.run_until_complete(app_close_event.wait())
