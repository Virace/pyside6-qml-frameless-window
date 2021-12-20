# -*- coding: utf-8 -*-
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @Site    : x-item.com
# @Software: Pycharm
# @Create  : 2021/12/14 13:47
# @Update  : 2021/12/16 18:52
# @Detail  : 窗体事件

import win32con
import win32gui
from PySide6.QtCore import QObject, Qt, Slot
from PySide6.QtQml import QmlElement
from PySide6.QtGui import QGuiApplication

QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class Function(QObject):

    @Slot()
    def max(self):
        for win in QGuiApplication.allWindows():
            if win.windowState() is Qt.WindowMaximized:
                win.showNormal()
            else:
                win.showMaximized()

    @Slot()
    def min(self):
        for win in QGuiApplication.allWindows():
            win.showMinimized()

    @Slot()
    def close(self):
        for win in QGuiApplication.allWindows():
            win.close()
