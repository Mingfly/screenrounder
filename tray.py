#tray.py
import sys
import os
import winreg
from PyQt6 import QtWidgets, QtGui, QtCore
from language import tr, get_language_list, set_language
from config import load_config, save_config, DEFAULT_CONFIG
from PyQt6.QtCore import QObject, pyqtSignal
from signals import language_signal
from utils import get_system_theme  # 导入获取系统主题的函数

class TrayApp(QtWidgets.QSystemTrayIcon):
    language_changed = pyqtSignal()
    theme_changed = pyqtSignal(str)  # 新增主题变化信号
    
    def __init__(self, icon, parent):
        super().__init__(icon, parent)
        self.setToolTip(tr("app_name"))
        self.parent = parent
        self.menu = QtWidgets.QMenu()
        
        # 存储子菜单引用
        self.color_menu = None
        self.lang_menu = None
        
        # 初始设置菜单样式
        self.current_theme = get_system_theme()
        self.update_menu_style()
        
        self.setContextMenu(self.menu)
        self.create_menu()
        self.activated.connect(self.on_tray_activated)
        
        # 添加主题变化检测定时器
        self.theme_timer = QtCore.QTimer(self)
        self.theme_timer.timeout.connect(self.check_theme_change)
        self.theme_timer.start(10000)  # 降低检测频率到10秒一次

    def check_theme_change(self):
        """检测系统主题是否变化"""
        new_theme = get_system_theme()
        if new_theme != self.current_theme:
            self.current_theme = new_theme
            self.update_menu_style()
            self.theme_changed.emit(new_theme)  # 发出主题变化信号
            
            # 如果主窗口存在，直接更新其主题
            if self.parent:
                self.parent.current_theme = new_theme
                self.parent.apply_theme()

    def update_menu_style(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        if self.current_theme == "dark":
            image_file = os.path.join(base_dir, "images", "checkmark-dark.svg")
        else:
            image_file = os.path.join(base_dir, "images", "checkmark-light.svg")

        # 把路径里的反斜杠换成正斜杠，避免路径错误
        image_path = image_file.replace("\\", "/")

        style = f"""
            QMenu {{
                background-color: {'#2d2d30' if self.current_theme == "dark" else '#f0f0f0'};
                color: {'#dcdcdc' if self.current_theme == "dark" else '#000000'};
                border: 1px solid {'#3f3f46' if self.current_theme == "dark" else '#b0b0b0'};
                border-radius: 8px;
                padding: 4px;
            }}
            
            QMenu QMenu {{
                background-color: {'#2d2d30' if self.current_theme == "dark" else '#f0f0f0'};
                border: 1px solid {'#3f3f46' if self.current_theme == "dark" else '#b0b0b0'};
                border-radius: 8px;
                margin: 0;
            }}
            
            QMenu::item {{
                padding: 6px 24px 6px 12px;
                border-radius: 4px;
                margin: 2px;
                background-color: transparent;
            }}
            
            QMenu::item:selected {{
                background-color: {'#3e3e42' if self.current_theme == "dark" else '#e0e0e0'};
                color: {'#ffffff' if self.current_theme == "dark" else '#000000'};
            }}
            
            QMenu::item:disabled {{
                color: #707070;
            }}
            
            QMenu::separator {{
                height: 1px;
                background-color: {'#3f3f46' if self.current_theme == "dark" else '#b0b0b0'};
                margin: 4px 8px;
            }}
            
            QMenu::indicator {{
                width: 16px;
                height: 16px;
                margin-right: 5px;
            }}
            
            QMenu::indicator:checked {{
                image: url("{image_path}");
            }}
        """

        self.menu.setStyleSheet(style)
        if self.color_menu:
            self.color_menu.setStyleSheet(style)
        if self.lang_menu:
            self.lang_menu.setStyleSheet(style)

        for menu in [self.menu, self.color_menu, self.lang_menu]:
            if menu:
                menu.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
                menu.setWindowFlags(
                    menu.windowFlags() | 
                    QtCore.Qt.WindowType.FramelessWindowHint |
                    QtCore.Qt.WindowType.NoDropShadowWindowHint
                )

    def on_tray_activated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.ActivationReason.DoubleClick:
            self.parent.show()
            self.parent.raise_()
            self.parent.activateWindow()

    def create_menu(self):
        """重建托盘菜单"""
        self.menu.clear()
        
        show_action = self.menu.addAction(tr("show_main"))
        show_action.triggered.connect(lambda: self.parent.show())

        refresh_action = self.menu.addAction(tr("refresh_monitors"))
        refresh_action.triggered.connect(lambda: self.parent.refresh_corners(force_reset=True))
        
        # 添加恢复默认值功能
        reset_action = self.menu.addAction(tr("reset_defaults"))
        reset_action.triggered.connect(self.reset_to_defaults)
        
        self.menu.addSeparator()

        self.color_menu = QtWidgets.QMenu(tr("corner_color"), self.menu)
        color_options = {
            tr("black"): QtGui.QColor(0, 0, 0),
            tr("white"): QtGui.QColor(255, 255, 255),
            tr("dark_gray"): QtGui.QColor(40, 40, 40),
            tr("light_gray"): QtGui.QColor(200, 200, 200),
            tr("dark_blue"): QtGui.QColor(0, 0, 80)
        }
        for name, color in color_options.items():
            action = self.color_menu.addAction(self.create_color_icon(color), name)
            action.triggered.connect(lambda checked=False, c=color: self.change_color(c))
        self.menu.addMenu(self.color_menu)
        
        self.lang_menu = QtWidgets.QMenu(tr("Language options"), self.menu)
        current_lang = self.parent.config.get("language", "en")
        
        for code, name in get_language_list():
            action = self.lang_menu.addAction(name)
            action.setCheckable(True)
            action.setChecked(code == current_lang)
            action.triggered.connect(lambda checked=False, c=code: self.change_language(c))
        self.menu.addMenu(self.lang_menu)
        
        self.menu.addSeparator()

        self.auto_start_action = self.menu.addAction(tr("autostart"))
        self.auto_start_action.setCheckable(True)
        self.auto_start_action.setChecked(self.is_auto_start_enabled())
        self.auto_start_action.triggered.connect(self.toggle_auto_start)

        help_action = self.menu.addAction(tr("help"))
        help_action.triggered.connect(self.show_help)
        
        exit_action = self.menu.addAction(tr("exit"))
        exit_action.triggered.connect(QtWidgets.QApplication.quit)
        
        self.update_menu_style()

    def reset_to_defaults(self):
        """将所有设置恢复为默认值"""
        # 获取默认配置
        default = DEFAULT_CONFIG
        
        # 更新主窗口中的控件值
        # 圆角半径设为10
        self.parent.radius_slider.setValue(default["radius"])
        
        # 圆角颜色设为纯黑色
        black_color = QtGui.QColor(*default["color"])
        self.parent.set_corner_color(black_color)
        
        # 防烧屏间隔设为10
        self.parent.burn_interval_spin.setValue(default["burn_in_interval"])
        
        # 启动防烧屏 - 勾选
        self.parent.anti_burn_check.setChecked(default["anti_burn_in"])
        
        # 隐藏圆角区域鼠标 - 勾选
        self.parent.mouse_check.setChecked(default["transparent_mouse"])
        
        # 启动时隐藏主界面 - 不勾选
        self.parent.hide_on_startup_check.setChecked(default["hide_on_startup"])
        
        # 关闭动作设为默认None
        self.parent.close_action = default["close_action"]
        self.parent.config["close_action"] = default["close_action"]
        
        # 保存所有更改
        save_config(self.parent.config)
        
        # 刷新圆角显示
        self.parent.refresh_corners()
        
        # 显示成功消息
        QtWidgets.QMessageBox.information(
            self.parent,
            tr("reset_success_title"),
            tr("reset_success_message"),
            QtWidgets.QMessageBox.StandardButton.Ok
        )

    def create_color_icon(self, color):
        pixmap = QtGui.QPixmap(16, 16)
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setBrush(QtGui.QBrush(color))
        painter.setPen(QtGui.QPen(QtGui.QColor(100, 100, 100), 1))
        painter.drawRoundedRect(1, 1, 14, 14, 4, 4)
        painter.end()
        return QtGui.QIcon(pixmap)

    def change_color(self, color: QtGui.QColor):
        self.parent.corner_color = color
        if hasattr(self.parent, 'color_preview'):
            self.parent.color_preview.setStyleSheet(
                f"background-color: {color.name()}; border: 1px solid #cccccc; border-radius: 4px;"
            )
        if hasattr(self.parent, 'corners'):
            for w in self.parent.corners:
                w.color = color
                w.update()
                w.hide()
                QtCore.QTimer.singleShot(50, w.show)
        self.parent.config["color"] = [color.red(), color.green(), color.blue()]
        save_config(self.parent.config)

    def change_language(self, lang_code):
        set_language(lang_code)
        self.parent.config["language"] = lang_code
        save_config(self.parent.config)
        self.create_menu()
        self.language_changed.emit()
        language_signal.changed.emit()

    def toggle_auto_start(self):
        if self.auto_start_action.isChecked():
            self.enable_auto_start()
        else:
            self.disable_auto_start()

    def enable_auto_start(self):
        exe_path = sys.executable
        script_path = os.path.abspath(sys.argv[0])
        cmd = f'"{exe_path}" "{script_path}"'
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "RoundedCorners", 0, winreg.REG_SZ, cmd)
            winreg.CloseKey(key)
        except Exception as e:
            print("[Autostart] 注册失败:", e)

    def disable_auto_start(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, "RoundedCorners")
            winreg.CloseKey(key)
        except FileNotFoundError:
            pass
        except Exception as e:
            print("[Autostart] 取消注册失败:", e)

    def is_auto_start_enabled(self):
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, 
                winreg.KEY_READ
            )
            try:
                value, _ = winreg.QueryValueEx(key, "RoundedCorners")
                exe_path = sys.executable
                script_path = os.path.abspath(sys.argv[0])
                expected_cmd = f'"{exe_path}" "{script_path}"'
                
                if value == expected_cmd:
                    return True
                normalized_value = value.replace('\\', '/').lower()
                normalized_expected = expected_cmd.replace('\\', '/').lower()
                if normalized_value == normalized_expected:
                    return True
            except FileNotFoundError:
                return False
            finally:
                winreg.CloseKey(key)
        except Exception:
            pass
        return False

    def show_help(self):
        msg_box = QtWidgets.QMessageBox(
            QtWidgets.QMessageBox.Icon.Information,
            tr("help_title"),
            tr("help_text"),
            QtWidgets.QMessageBox.StandardButton.Ok,
            parent=self.parent
        )
        ok_button = msg_box.button(QtWidgets.QMessageBox.StandardButton.Ok)
        ok_button.setText(tr("acknowledge"))
        msg_box.exec()
