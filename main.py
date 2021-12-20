# -*- coding: utf-8 -*-
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @Site    : x-item.com
# @Software: Pycharm
# @Create  : 2021/12/14 0:32
# @Update  : 2021/12/16 16:33
# @Detail  : 

from pathlib import Path
from gui import MyGUI

from slot.window import Function


if __name__ == '__main__':
    a = MyGUI()
    
    a.start(Path(__file__).parent / 'main.qml')

