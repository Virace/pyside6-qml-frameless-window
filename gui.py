# -*- coding: utf-8 -*-
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @Site    : x-item.com
# @Software: Pycharm
# @Create  : 2021/12/13 23:56
# @Update  : 2021/12/16 18:52
# @Detail  : GUI初始化

import sys

from PySide6.QtCore import QAbstractNativeEventFilter
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from repair.Windows import WindowEffect, WindowsEventFilter


class MyGUI:
    def __init__(self, event_filter: QAbstractNativeEventFilter = None, context=None):

        if context is None:
            context = {}
        # 初始化
        self.app = QGuiApplication(sys.argv)
        self.engine = QQmlApplicationEngine()
        self.wef = WindowsEventFilter(5)
        self.app.installNativeEventFilter(self.wef)
        if event_filter:
            self.app.installNativeEventFilter(event_filter)

        if context:
            root = self.engine.rootContext()
            for k, v in context.items():
                root.setContextProperty(k, v)
        self.win_rep = WindowEffect()

    def start(self, file):
        # 加载qml文件
        self.engine.load(file)
        self._on_load_after()
        if not self.engine.rootObjects():
            sys.exit(-1)
        sys.exit(self.app.exec())

    def _on_load_after(self):
        # windows 恢复特效
        if sys.platform == 'win32':
            for win in self.app.allWindows():
                self.win_rep.addShadowEffect(win.winId())
                self.win_rep.addWindowAnimation(win.winId())
                self.win_rep.setAcrylicEffect(win.winId())

