from PySide2.QtCore import QObject, Signal, Slot
from util import logthread


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
