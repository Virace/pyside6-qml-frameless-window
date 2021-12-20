# -*- coding: utf-8 -*-
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @Site    : x-item.com
# @Software: Pycharm
# @Create  : 2021/12/13 23:25
# @Update  : 2021/12/16 18:50
# @Detail  : Windows 窗口修复

# https://github.com/zhiyiYo/PyQt-Frameless-Window/blob/master/windoweffect/window_effect.py

from ctypes import POINTER, WinDLL, byref, c_bool, c_int, pointer, sizeof
from ctypes.wintypes import DWORD, LONG, LPCVOID

import win32api
import win32con
import win32gui

from .c_structures import (
    ACCENT_POLICY,
    ACCENT_STATE,
    DWMNCRENDERINGPOLICY,
    DWMWINDOWATTRIBUTE,
    MARGINS,
    WINDOWCOMPOSITIONATTRIB,
    WINDOWCOMPOSITIONATTRIBDATA)


class WindowEffect:
    """ A class that calls Windows API to realize window effect """

    def __init__(self):
        # Declare the function signature of the API
        self.user32 = WinDLL("user32")
        self.dwmapi = WinDLL("dwmapi")
        self.SetWindowCompositionAttribute = self.user32.SetWindowCompositionAttribute
        self.DwmExtendFrameIntoClientArea = self.dwmapi.DwmExtendFrameIntoClientArea
        self.DwmSetWindowAttribute = self.dwmapi.DwmSetWindowAttribute
        self.SetWindowCompositionAttribute.restype = c_bool
        self.DwmExtendFrameIntoClientArea.restype = LONG
        self.DwmSetWindowAttribute.restype = LONG
        self.SetWindowCompositionAttribute.argtypes = [
            c_int,
            POINTER(WINDOWCOMPOSITIONATTRIBDATA),
        ]
        self.DwmSetWindowAttribute.argtypes = [c_int, DWORD, LPCVOID, DWORD]
        self.DwmExtendFrameIntoClientArea.argtypes = [c_int, POINTER(MARGINS)]
        # Initialize structure
        self.accentPolicy = ACCENT_POLICY()
        self.winCompAttrData = WINDOWCOMPOSITIONATTRIBDATA()
        self.winCompAttrData.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY.value[0]
        self.winCompAttrData.SizeOfData = sizeof(self.accentPolicy)
        self.winCompAttrData.Data = pointer(self.accentPolicy)

    def setAcrylicEffect(
            self,
            hWnd,
            gradientColor: str = "F2F2F299",
            isEnableShadow: bool = True,
            animationId: int = 0):
        """ Add the acrylic effect to the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle

        gradientColor: str
            Hexadecimal acrylic mixed color, corresponding to four RGBA channels

        isEnableShadow: bool
            Enable window shadows

        animationId: int
            Turn on matte animation
        """
        # Acrylic mixed color
        gradientColor = (
                gradientColor[6:]
                + gradientColor[4:6]
                + gradientColor[2:4]
                + gradientColor[:2]
        )
        gradientColor = DWORD(int(gradientColor, base=16))
        # matte animation
        animationId = DWORD(animationId)
        # window shadow
        accentFlags = DWORD(0x20 | 0x40 | 0x80 |
                            0x100) if isEnableShadow else DWORD(0)
        self.accentPolicy.AccentState = ACCENT_STATE.ACCENT_ENABLE_ACRYLICBLURBEHIND.value[0]
        self.accentPolicy.GradientColor = gradientColor
        self.accentPolicy.AccentFlags = accentFlags
        self.accentPolicy.AnimationId = animationId
        # enable acrylic effect
        self.SetWindowCompositionAttribute(hWnd, pointer(self.winCompAttrData))

    def setAeroEffect(self, hWnd):
        """ Add the aero effect to the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        self.accentPolicy.AccentState = ACCENT_STATE.ACCENT_ENABLE_BLURBEHIND.value[0]
        # enable Aero effect
        self.SetWindowCompositionAttribute(hWnd, pointer(self.winCompAttrData))

    def removeBackgroundEffect(self, hWnd):
        """ Remove background effect

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        self.accentPolicy.AccentState = ACCENT_STATE.ACCENT_DISABLED.value[0]
        self.SetWindowCompositionAttribute(hWnd, pointer(self.winCompAttrData))

    @staticmethod
    def moveWindow(hWnd):
        """ Move the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        win32gui.ReleaseCapture()
        win32api.SendMessage(
            hWnd,
            win32con.WM_SYSCOMMAND,
            win32con.SC_MOVE +
            win32con.HTCAPTION,
            0)

    def addShadowEffect(self, hWnd):
        """ Add DWM shadow to the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        self.DwmSetWindowAttribute(
            hWnd,
            DWMWINDOWATTRIBUTE.DWMWA_NCRENDERING_POLICY.value,
            byref(c_int(DWMNCRENDERINGPOLICY.DWMNCRP_ENABLED.value)),
            4,
        )
        margins = MARGINS(-1, -1, -1, -1)
        self.DwmExtendFrameIntoClientArea(hWnd, byref(margins))

    def removeShadowEffect(self, hWnd):
        """ Remove DWM shadow from the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        self.DwmSetWindowAttribute(
            hWnd,
            DWMWINDOWATTRIBUTE.DWMWA_NCRENDERING_POLICY.value,
            byref(c_int(DWMNCRENDERINGPOLICY.DWMNCRP_DISABLED.value)),
            4,
        )

    @staticmethod
    def removeMenuShadowEffect(hWnd):
        """ Remove shadow from pop-up menu

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        style = win32gui.GetClassLong(hWnd, win32con.GCL_STYLE)
        style &= ~0x00020000  # CS_DROPSHADOW
        win32api.SetClassLong(hWnd, win32con.GCL_STYLE, style)

    @staticmethod
    def addWindowAnimation(hWnd):
        """ Enables the maximize and minimize animation of the window

        Parameters
        ----------
        hWnd : int or `sip.voidptr`
            Window handle
        """
        style = win32gui.GetWindowLong(hWnd, win32con.GWL_STYLE)

        win32gui.SetWindowLong(
            hWnd,
            win32con.GWL_STYLE,
            style
            | win32con.WS_MAXIMIZEBOX
            | win32con.WS_CAPTION
            | win32con.CS_DBLCLKS
            | win32con.WS_THICKFRAME,
        )

        style = win32gui.GetWindowLong(hWnd, win32con.GWL_EXSTYLE)
        style &= ~win32con.WS_EX_LAYERED
        win32gui.SetWindowLong(
            hWnd,
            win32con.GWL_EXSTYLE,
            style
        )
        # win32gui.AnimateWindow(hWnd, 2000, win32con.AW_BLEND | win32con.AW_ACTIVATE)
