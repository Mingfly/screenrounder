# signals.py
from PyQt6.QtCore import QObject, pyqtSignal

class LanguageSignal(QObject):
    changed = pyqtSignal()

language_signal = LanguageSignal()