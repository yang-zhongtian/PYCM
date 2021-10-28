from PyQt5.QtCore import QLocale

SUPPORTED_TRANSLATION = ['zh_CN']


def load_translation():
    language = QLocale.system().name()
    if language in SUPPORTED_TRANSLATION:
        return language
    else:
        return None
