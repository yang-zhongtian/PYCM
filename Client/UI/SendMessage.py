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
from PyQt5.QtCore import Qt, QCoreApplication
import socket
from .SendMessageUI import Ui_SendMessageForm


class SendMessageForm(QWidget):
    _translate = QCoreApplication.translate

    def __init__(self, parent=None):
        super(SendMessageForm, self).__init__()
        self.parent = parent
        self.ui = Ui_SendMessageForm()
        self.ui.setupUi(self)

    def add_message(self, is_receive, message):
        if is_receive:
            direction = self._translate('SendMessageForm', 'Received')
        else:
            direction = self._translate('SendMessageForm', 'Send')
        self.ui.message_area.append('%s: %s' % (direction, message))

    def send_message(self):
        message = self.ui.message_input.text()
        self.parent.private_message_object.send_message(message)
        self.add_message(False, message)
        self.ui.message_input.clear()

    def update_input_text(self):
        self.ui.send.setEnabled(len(self.ui.message_input.text()) > 0)
