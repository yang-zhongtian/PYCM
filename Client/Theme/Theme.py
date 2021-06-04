from PyQt5.QtCore import QCoreApplication, QFile, QTextStream, QT_VERSION_STR
from PyQt5.QtGui import QColor, QPalette, QFontDatabase, QFont
from Theme.light import style_rc
from Theme.light.palette import LightPalette
import os
import platform
import sys

palette = LightPalette


def _apply_os_patches(palette):
    os_fix = ""
    if platform.system().lower() == 'darwin':
        os_fix = '''
        QDockWidget::title
        {{
            background-color: {color};
            text-align: center;
            height: 12px;
        }}
        QTabBar::close-button {{
            padding: 2px;
        }}
        '''.format(color=palette.COLOR_BACKGROUND_4)
    return os_fix


def _apply_customize_patches():
    general_fix = '''
        QPushButton {
            padding: 6px 6px;
            height: 25px;
        }
        QGroupBox {
            padding: 8px;
        }
        QGroupBox::title {
            top: 2px;
        }
    '''
    translation_fix = '''
        QMessageBox QPushButton[text="OK"] {
            qproperty-text: "好的";
        }
        QMessageBox QPushButton[text="Open"] {
            qproperty-text: "打开";
        }
        QMessageBox QPushButton[text="Save"] {
            qproperty-text: "保存";
        }
        QMessageBox QPushButton[text="Cancel"] {
            qproperty-text: "取消";
        }
        QMessageBox QPushButton[text="Close"] {
            qproperty-text: "关闭";
        }
        QMessageBox QPushButton[text="Discard"] {
            qproperty-text: "不保存";
        }
        QMessageBox QPushButton[text="Don't Save"] {
            qproperty-text: "不保存";
        }
        QMessageBox QPushButton[text="Apply"] {
            qproperty-text: "应用";
        }
        QMessageBox QPushButton[text="Reset"] {
            qproperty-text: "重置";
        }
        QMessageBox QPushButton[text="Restore Defaults"] {
            qproperty-text: "恢复默认";
        }
        QMessageBox QPushButton[text="Help"] {
            qproperty-text: "帮助";
        }
        QMessageBox QPushButton[text="Save All"] {
            qproperty-text: "保存全部";
        }
        QMessageBox QPushButton[text="&Yes"] {
            qproperty-text: "是";
        }
        QMessageBox QPushButton[text="Yes to &All"] {
            qproperty-text: "全部都是";
        }
        QMessageBox QPushButton[text="&No"] {
            qproperty-text: "否";
        }
        QMessageBox QPushButton[text="N&o to All"] {
            qproperty-text: "全部都不";
        }
        QMessageBox QPushButton[text="Abort"] {
            qproperty-text: "终止";
        }
        QMessageBox QPushButton[text="Retry"] {
            qproperty-text: "重试";
        }
        QMessageBox QPushButton[text="Ignore"] {
            qproperty-text: "忽略";
        }
    '''
    return general_fix + translation_fix


def _apply_version_patches(qt_version):
    version_fix = ''
    major, minor, patch = qt_version.split('.')
    major, minor, patch = int(major), int(minor), int(patch)
    if major == 5 and minor >= 14:
        version_fix = '''
        QMenu::item {
            padding: 4px 24px 4px 6px;
        }
        '''
    return version_fix


def _apply_application_patches(q_core_application, q_palette, q_color, palette):
    color = palette.COLOR_ACCENT_3
    qcolor = q_color(color)
    app = q_core_application.instance()
    app_palette = app.palette()
    app_palette.setColor(q_palette.Normal, q_palette.Link, qcolor)
    app.setPalette(app_palette)


def load_stylesheet():
    qss_rc_path = ':' + os.path.join('qdarkstyle', palette.ID, 'style.qss')
    qss_file = QFile(qss_rc_path)
    qss_file.open(QFile.ReadOnly | QFile.Text)
    text_stream = QTextStream(qss_file)
    stylesheet = text_stream.readAll()

    stylesheet += _apply_os_patches(palette)
    stylesheet += _apply_version_patches(QT_VERSION_STR)
    stylesheet += _apply_customize_patches()
    _apply_application_patches(QCoreApplication, QPalette, QColor, palette)

    return stylesheet


def load_font():
    QFontDatabase.addApplicationFont('SourceHanSansSC-VF.ttf')
    font = QFont('Source Han Sans SC VF')
    font.setPointSize(10)
    return font
