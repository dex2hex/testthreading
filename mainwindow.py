from PySide2.QtWidgets import QMainWindow
from uiloader import loadUi
from PySide2.QtCore import QThread, Slot, Signal
from PySide2.QtGui import QCloseEvent
from util import logthread
from worker import Worker


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        logthread('MainWindow.__init__')
        QMainWindow.__init__(self, parent)
        self.widget = loadUi('window.ui', self)
        self.setFixedSize(self.size())

        self.thread = QThread()
        self.thread.started.connect(self.threadStarted)
        self.thread.finished.connect(self.threadFinished)

        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        self.thread.start()

        self.worker.qtextedit.connect(self.qtextedit_addtext)
        self.worker.stop.connect(self.endNow)
        self.worker.progress.connect(self.updateProgressBar)

    @Slot()
    def on_pbStart_clicked(self):
        logthread('MainWindow.on_pbStart_clicked')
        self.widget.pbrProgress.setRange(0, 0)

        self.teErrors.setText("")

        self.worker.start.emit()

    @Slot()
    def on_pbStop_clicked(self):
        logthread('MainWindow.on_pbStop_clicked')
        self.widget.pbrProgress.setRange(0, 1)

        self.worker.stop.emit()

    @Slot(str)
    def qtextedit_addtext(self, text):
        logthread('MainWindow.qtextedit_addtext args-{}'.format(str(text)))
        self.teErrors.setText(str(text))

    @Slot()
    def endNow(self):
        logthread('MainWindow.endNow')
        self.worker.continueWork = False

    @Slot(int)
    def updateProgressBar(self, progress):
        logthread('MainWindow.updateProgressBar')
        self.widget.pbrProgress.setValue(progress)

    @Slot()
    def on_actionProject1_triggered(self):
        logthread('MainWindow.on_actionProject1_triggered')

        from projectsettings1 import SettingsProject1
        dialogSettingsProject1 = SettingsProject1()
        dialogSettingsProject1.exec_()

    @Slot()
    def on_actionProject2_triggered(self):
        logthread('MainWindow.on_actionProject2_triggered')

        from projectsettings2 import SettingsProject2
        dialogSettingsProject2 = SettingsProject2()
        dialogSettingsProject2.exec_()

    def closeEvent(self, event: QCloseEvent):
        logthread('MainWindow.closeEvent')
        self.worker.continueWork = False
        self.thread.quit()
        self.thread.wait()

    def threadStarted(self):
        logthread('MainWindow.threadStarted')

    def threadFinished(self):
        logthread('MainWindow.threadFinished')
