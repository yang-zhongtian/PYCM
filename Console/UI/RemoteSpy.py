# -*- coding: utf-8 -*-
"""
    This file is part of PYCM project
    Copyright (C) 2021 Richard Yang  <zhongtian.yang@qq.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QResizeEvent, QCloseEvent
from .RemoteSpyUI import Ui_RemoteSpy


class RemoteSpyForm(QWidget):
    def __init__(self, parent=None):
        super(RemoteSpyForm, self).__init__()
        self.parent = parent
        self.frame_proportion = 9 / 16
        self.ui = Ui_RemoteSpy()
        self.ui.setupUi(self)
        self.ui.screen_display.move(0, 0)

    def update_frame(self, frame):
        screen_display_object = self.ui.screen_display
        screen_display_object.setPixmap(frame)

    def resizeEvent(self, event: QResizeEvent):
        container_size = self.size()
        container_height = container_size.height()
        container_width = container_size.width()
        container_proportion = container_height / container_width
        screen_height = container_height
        screen_width = container_width
        if container_proportion > self.frame_proportion:
            container_height = int(screen_width * self.frame_proportion)
        elif container_proportion < self.frame_proportion:
            container_width = int(screen_height / self.frame_proportion)
        self.ui.screen_display.resize(container_width, container_height)
        self.resize(container_width, container_height)

    def closeEvent(self, event: QCloseEvent):
        self.parent.toggle_remote_spy(False)
