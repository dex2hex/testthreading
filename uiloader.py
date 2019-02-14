from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QMetaObject


class UiLoader(QUiLoader):
    def __init__(self, baseInstance, customWidgets=None):
        QUiLoader.__init__(self, baseInstance)
        self.baseInstance = baseInstance
        self.customWidgets = customWidgets

    def createWidget(self, className, parent=None, name=''):
        if parent is None and self.baseInstance:
            return self.baseInstance
        else:
            if className in self.availableWidgets():
                widget = QUiLoader.createWidget(self, className, parent, name)
            else:
                try:
                    widget = self.customWidgets[className](parent)
                except (TypeError, KeyError) as e:
                    raise Exception('No custom widget {className} found in customWidgets param of UiLoader __init__.'.format(className=className))

                if self.baseInstance:
                    setattr(self.baseInstance, name, widget)
                    print(name)

            return widget


def loadUi(uiFile, baseInstance=None, customWidgets=None):
    loader = UiLoader(baseInstance, customWidgets)
    widget = loader.load(uiFile)
    QMetaObject.connectSlotsByName(widget)
    return widget


