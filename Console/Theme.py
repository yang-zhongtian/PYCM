from PyQt5.QtCore import QCoreApplication, QFile, QTextStream, QT_VERSION_STR
from PyQt5.QtGui import QColor, QPalette, QFontDatabase
import platform
import os


def _apply_os_patches():
    os_fix = ''
    if platform.system().lower() == 'darwin':
        os_fix = '''
        QDockWidget::title
        {{
            background-color: #455364;
            text-align: center;
            height: 12px;
        }}
        QTabBar::close-button {{
            padding: 2px;
        }}
        '''
    return os_fix


def _apply_version_patches():
    version_fix = ''
    major, minor, patch = QT_VERSION_STR.split('.')
    major, minor, patch = int(major), int(minor), int(patch)
    if major == 5 and minor >= 14:
        version_fix = '''
        QMenu::item {
            padding: 4px 24px 4px 6px;
        }
        '''
    return version_fix


def _apply_application_patches():
    app = QCoreApplication.instance()
    app_palette = app.palette()
    app_palette.setColor(QPalette.Normal, QPalette.Link, QColor('#1A72BB'))
    app.setPalette(app_palette)


def _apply_application_font():
    current_path = os.path.dirname(os.path.abspath(__file__))
    QFontDatabase.addApplicationFont(os.path.join(current_path, 'Alibaba-PuHuiTi-Regular.ttf'))
    QFontDatabase.addApplicationFont(os.path.join(current_path, 'Alibaba-PuHuiTi-Bold.ttf'))


def load_stylesheet():
    qss_file = QFile(':/Core/Style.qss')
    qss_file.open(QFile.ReadOnly | QFile.Text)
    text_stream = QTextStream(qss_file)
    text_stream.setCodec('UTF-8')
    stylesheet = text_stream.readAll()

    stylesheet += _apply_os_patches()
    stylesheet += _apply_version_patches()
    _apply_application_patches()
    _apply_application_font()

    return stylesheet
