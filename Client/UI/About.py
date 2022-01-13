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

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QCoreApplication
from .AboutUI import Ui_AboutDialog

try:
    from BuildInfo import BUILD_INFO
except ImportError:
    BUILD_INFO = None


class AboutDialog(QDialog):
    _translate = QCoreApplication.translate

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.ui = Ui_AboutDialog()
        self.parent = parent
        self.ui.setupUi(self)
        build_info = BUILD_INFO
        if build_info is None:
            build_info = self._translate('AboutDialog', 'No build info')
        self.ui.buildInfo.setText(self._translate('AboutDialog', 'Build Info: %s') % BUILD_INFO)
