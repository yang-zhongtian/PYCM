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

from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtCore import Qt, QCoreApplication, QDir
from PyQt5.QtGui import QPaintEvent, QCloseEvent
from .ScreenBroadcastUI import Ui_ScreenBroadcastForm


class ScreenBroadcastForm(QWidget):
    parent = None
    freeze = False
    first_frame = True
    _translate = QCoreApplication.translate

    def __init__(self, parent=None):
        super(ScreenBroadcastForm, self).__init__()
        self.parent = parent
        self.frame_proportion = 9 / 16
        self.ui = Ui_ScreenBroadcastForm()
        self.ui.setupUi(self)
        self.ui.screen_display.move(0, 0)
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowStaysOnTopHint)

    def update_frame(self, frame):
        if not self.freeze:
            screen_display_object = self.ui.screen_display
            screen_display_object.setPixmap(frame)
        if self.first_frame:
            self.frame_proportion = frame.height() / frame.width()
            self.first_frame = False

    def freeze_frame(self, freeze=True):
        self.freeze = freeze

    def show_full_screen(self, fullscreen=True):
        if fullscreen:
            self.showFullScreen()
        else:
            self.showNormal()

    def screen_shot(self):
        frame = self.ui.screen_display.pixmap()
        frame = frame.toImage()
        file_path, _ = QFileDialog.getSaveFileName(self, self._translate('ScreenBroadcastForm', 'Select Path To Save'),
                                                   str(QDir.homePath()),
                                                   self._translate('ScreenBroadcastForm', 'JPEG Image(*.jpg)'))
        if file_path:
            frame.save(file_path, 'JPEG')

    def toggle_always_on_top(self, on_top):
        self.windowHandle().setFlag(Qt.WindowStaysOnTopHint, on_top)

    def paintEvent(self, event: QPaintEvent):
        container_size = self.ui.screen_widget.size()
        container_height = container_size.height()
        container_width = container_size.width()
        container_proportion = container_height / container_width
        screen_height = container_height
        screen_width = container_width
        if container_proportion > self.frame_proportion:
            screen_height = int(screen_width * self.frame_proportion)
            delta_height = container_height - screen_height
            self.ui.screen_display.move(0, delta_height // 2)
        elif container_proportion < self.frame_proportion:
            screen_width = int(screen_height / self.frame_proportion)
            delta_width = container_width - screen_width
            self.ui.screen_display.move(delta_width // 2, 0)
        self.ui.screen_display.resize(screen_width, screen_height)

    def closeEvent(self, event: QCloseEvent):
        event.ignore()
