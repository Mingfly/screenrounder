# utils.py
import os
import sys
import locale
import ctypes
import platform
import winreg


def get_icon_path():
    """查找程序图标路径"""
    paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "icon.png"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png"),
        os.path.join(os.path.dirname(sys.executable), "resources", "icon.png"),
        os.path.join(os.path.dirname(sys.executable), "icon.png"),
    ]
    for path in paths:
        if os.path.exists(path):
            return path
    return ""


def get_system_language(supported_langs=None):
    """获取系统语言代码"""
    try:
        lang = locale.getdefaultlocale()[0]
        if lang:
            lang_code = lang.split('_')[0]
            if supported_langs and lang_code not in supported_langs:
                return "en"
            return lang_code
    except:
        pass
    return "en"


def get_system_theme():
    """检测当前 Windows 主题（light/dark）"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        )
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return "light" if value == 1 else "dark"
    except:
        return "light"


def get_idle_duration_seconds():
    """获取系统空闲时间（单位：秒）"""
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(lii)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return millis / 1000


def is_windows_11_or_higher():
    """检查是否为 Windows 11 或更高版本"""
    return sys.platform == "win32" and int(platform.release()) >= 10
