import sys
import os
import platform
import atexit
import tempfile
from PyQt6 import QtWidgets, QtGui, QtCore
from main_window import MainWindow
from tray import TrayApp
from utils import get_icon_path
from language import tr, set_language, CURRENT_LANG
from config import load_config
from signals import language_signal

class SingleInstance:
    def __init__(self, app_id):
        self.app_id = app_id
        self.lockfile = None
        self.is_running = False
        
        # 锁文件路径（跨平台）
        self.lockfile = os.path.join(
            tempfile.gettempdir(), 
            f"{app_id}.lock" if sys.platform == "win32" else f".{app_id}.lock"
        )
        
        self.check()
    
    def check(self):
        """检查是否已有实例运行"""
        try:
            if sys.platform == "win32":
                # Windows实现
                if os.path.exists(self.lockfile):
                    try:
                        with open(self.lockfile, "r") as f:
                            pid = int(f.read())
                        if self._is_process_running(pid):
                            self.is_running = True
                            return
                        # 清理无效锁文件
                        os.remove(self.lockfile)
                    except:
                        # 锁文件无效，删除它
                        try:
                            os.remove(self.lockfile)
                        except:
                            pass
                
                # 创建新锁文件
                with open(self.lockfile, "w") as f:
                    f.write(str(os.getpid()))
            else:
                # Unix实现
                self.fd = open(self.lockfile, "w")
                try:
                    import fcntl
                    fcntl.lockf(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    self.fd.write(str(os.getpid()))
                    self.fd.flush()
                except:
                    self.is_running = True
                    return
            
            # 确保注册清理函数
            atexit.register(self.cleanup)
            
        except Exception as e:
            print(f"防多开检查出错: {e}")
            self.is_running = True
    
    def _is_process_running(self, pid):
        """检查进程是否存在"""
        try:
            if sys.platform == "win32":
                import ctypes
                PROCESS_QUERY_INFORMATION = 0x0400
                handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, pid)
                if handle != 0:
                    ctypes.windll.kernel32.CloseHandle(handle)
                    return True
                return False
            else:
                os.kill(pid, 0)
                return True
        except:
            return False
    
    def cleanup(self):
        """退出时清理锁文件"""
        try:
            print(f"正在清理锁文件: {self.lockfile}")
            if sys.platform == "win32":
                if os.path.exists(self.lockfile):
                    os.remove(self.lockfile)
            else:
                if hasattr(self, 'fd'):
                    self.fd.close()
                if os.path.exists(self.lockfile):
                    os.remove(self.lockfile)
        except Exception as e:
            print(f"清理锁文件失败: {e}")

def create_warning_dialog():
    """创建并返回一个配置好的警告对话框（支持多语言刷新）"""
    # 创建消息框
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
    msg.setWindowTitle(tr("already_running_title"))
    
    # 设置图标
    icon_path = get_icon_path()
    if icon_path and os.path.exists(icon_path):
        msg.setWindowIcon(QtGui.QIcon(icon_path))
    
    # 使用tr()获取多语言文本
    msg.setText(tr("already_running_message"))
    msg.setInformativeText(tr("already_running_info"))
    
    ok_button = msg.addButton(tr("confirm_button"), QtWidgets.QMessageBox.ButtonRole.AcceptRole)
    msg.setDefaultButton(ok_button)
    
    # 设置窗口置顶
    msg.setWindowFlags(msg.windowFlags() | QtCore.Qt.WindowType.WindowStaysOnTopHint)
    
    # 定义刷新文本的函数
    def reload_texts():
        msg.setWindowTitle(tr("already_running_title"))
        msg.setText(tr("already_running_message"))
        msg.setInformativeText(tr("already_running_info"))
        ok_button.setText(tr("confirm_button"))
    
    # 连接语言更改信号
    language_signal.changed.connect(reload_texts)
    
    # 确保对话框关闭时断开信号连接
    def on_finished():
        language_signal.changed.disconnect(reload_texts)
    msg.finished.connect(on_finished)
    
    return msg

def is_system_dark_mode():
    """检测系统是否处于深色模式"""
    if sys.platform == "win32":
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return value == 0
        except:
            return False
    elif sys.platform == "darwin":
        try:
            # macOS 检测
            from Foundation import NSUserDefaults
            return NSUserDefaults.standardUserDefaults().stringForKey_("AppleInterfaceStyle") == "Dark"
        except ImportError:
            # 如果没有pyobjc，使用回退方法
            return False
    else:
        # Linux 系统检测
        return os.environ.get("GTK_THEME", "").endswith("-dark") or \
               os.environ.get("COLORFGBG", "").startswith("15;") or \
               os.environ.get("DARK_MODE", "") == "1"

def apply_system_theme(app):
    """应用系统主题设置"""
    # Windows 10+ 使用Fusion样式
    if sys.platform == "win32" and int(platform.release()) >= 10:
        app.setStyle("Fusion")
    
    # 适配深色模式
    if is_system_dark_mode():
        # 深色模式调色板
        dark_palette = QtGui.QPalette()
        dark_palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(53, 53, 53))
        dark_palette.setColor(QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white)
        dark_palette.setColor(QtGui.QPalette.ColorRole.Base, QtGui.QColor(35, 35, 35))
        dark_palette.setColor(QtGui.QPalette.ColorRole.AlternateBase, QtGui.QColor(53, 53, 53))
        dark_palette.setColor(QtGui.QPalette.ColorRole.ToolTipBase, QtCore.Qt.GlobalColor.white)
        dark_palette.setColor(QtGui.QPalette.ColorRole.ToolTipText, QtCore.Qt.GlobalColor.white)
        dark_palette.setColor(QtGui.QPalette.ColorRole.Text, QtCore.Qt.GlobalColor.white)
        dark_palette.setColor(QtGui.QPalette.ColorRole.Button, QtGui.QColor(53, 53, 53))
        dark_palette.setColor(QtGui.QPalette.ColorRole.ButtonText, QtCore.Qt.GlobalColor.white)
        dark_palette.setColor(QtGui.QPalette.ColorRole.BrightText, QtCore.Qt.GlobalColor.red)
        dark_palette.setColor(QtGui.QPalette.ColorRole.Link, QtGui.QColor(42, 130, 218))
        dark_palette.setColor(QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(142, 45, 197).lighter())
        dark_palette.setColor(QtGui.QPalette.ColorRole.HighlightedText, QtCore.Qt.GlobalColor.black)
        app.setPalette(dark_palette)
        
        # 额外设置工具提示样式
        app.setStyleSheet("""
            QToolTip {
                color: #ffffff;
                background-color: #2a82da;
                border: 1px solid white;
            }
        """)
    else:
        # 浅色模式使用系统默认
        app.setStyleSheet("")

def show_warning():
    """显示重复启动警告框（支持多语言和主题）"""
    config = load_config()
    set_language(config.get("language", "en"))  # 使用配置中的语言，默认英语
    
    # 创建应用实例
    app = QtWidgets.QApplication(sys.argv)
    
    # 应用系统主题适配
    apply_system_theme(app)
    
    # 创建并显示警告对话框
    warning_dialog = create_warning_dialog()
    
    # 监听系统主题变化
    palette = app.palette()
    palette_changed = False
    
    def update_dialog_theme():
        nonlocal palette_changed
        current_palette = app.palette()
        if current_palette != palette or not palette_changed:
            palette_changed = True
            warning_dialog.setPalette(current_palette)
            # 强制刷新样式
            warning_dialog.style().unpolish(warning_dialog)
            warning_dialog.style().polish(warning_dialog)
            warning_dialog.update()
    
    # 初始设置主题
    update_dialog_theme()
    
    # 监听主题变化
    app.paletteChanged.connect(update_dialog_theme)
    
    # 显示对话框
    warning_dialog.exec()
    
    # 确保应用完全退出
    QtCore.QTimer.singleShot(0, app.quit)
    app.exec()

def main():
    # 唯一实例检查
    instance = SingleInstance("RoundedCorners_UniqueID")
    if instance.is_running:
        show_warning()  # 显示本地化警告
        return  # 直接退出，不继续执行

    # 正常启动流程
    app = QtWidgets.QApplication(sys.argv)
    
    # 初始化配置和语言
    config = load_config()
    set_language(config.get("language", "en"))
    
    # 应用系统主题
    apply_system_theme(app)

    # Windows风格设置
    if sys.platform == "win32" and int(platform.release()) >= 10:
        app.setStyle("Fusion")

    # 初始化主窗口
    window = MainWindow()
    
    # 创建托盘图标，传入主窗口作为父对象
    icon = QtGui.QIcon(get_icon_path()) if get_icon_path() else QtGui.QIcon()
    tray_icon = TrayApp(icon, window)  # 传入主窗口作为父对象
    tray_icon.show()
    window.tray_icon = tray_icon

    # 连接主题变化信号
    tray_icon.theme_changed.connect(window.on_theme_changed)

    # 添加语言改变信号处理
    def on_language_changed():
        # 重新加载配置和语言
        config = load_config()
        set_language(config.get("language", "en"))
        
        # 刷新主窗口UI
        window.update_ui_language()
        
        # 刷新圆角窗口
        window.refresh_corners()
        
        # 发出全局语言改变信号
        language_signal.changed.emit()

    # 连接信号
    tray_icon.language_changed.connect(on_language_changed)
    
    # 显示主窗口
    if not window.hide_on_startup:
        window.show()

    # 确保应用退出时清理锁文件
    app.aboutToQuit.connect(instance.cleanup)
    
    app.setQuitOnLastWindowClosed(False)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()