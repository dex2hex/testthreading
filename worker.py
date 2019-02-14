from PySide2.QtCore import QObject, Signal, Slot
from util import logthread
import time


class Worker(QObject):

    start = Signal()
    stop = Signal()

    progress = Signal(int)

    qtextedit = Signal(str)

    def __init__(self):
        logthread('Worker.__init__')
        super().__init__()

        self.continueWork = True

        self.start.connect(self.startNow)

        self.process = None

    @Slot()
    def startNow(self):
        logthread('Worker.startNow')

        self.continueWork = True

        try:
            self.do_heavy_task()
        except Exception as e:
            print(str(e))

    def do_heavy_task(self):
        count = 0
        while self.continueWork is True:
            count += 1
            
            # https://bugreports.qt.io/browse/PYSIDE-803?focusedCommentId=424945&page=com.atlassian.jira.plugin.system.issuetabpanels:comment-tabpanel#comment-424945
            # time.sleep(0)
