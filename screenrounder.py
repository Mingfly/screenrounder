import sys
import os
import ctypes
from PyQt6 import QtWidgets, QtCore, QtGui
import winreg
import json
import platform
import random
import time

# 添加互斥锁防止多开
mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "RoundedCornersBeautifierMutex")
last_error = ctypes.windll.kernel32.GetLastError()
if last_error == 183:  # ERROR_ALREADY_EXISTS
    QtWidgets.QMessageBox.warning(None, "Error", "程序已在运行中！")
    sys.exit(1)

# 配置文件路径
CONFIG_PATH = os.path.join(os.path.expanduser("~"), "RoundedCornersConfig.json")

# DPI 适配（高分屏）
if sys.platform == "win32":
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

# 多语言支持
LANGUAGES = {
    "zh": {
        "language_name": "中文",
        "app_name": "屏幕圆角美化工具",
        "tray_tooltip": "屏幕圆角美化工具",
        "show_main": "显示主界面",
        "refresh_monitors": "刷新显示器",
        "corner_color": "圆角颜色",
        "autostart": "开机启动",
        "help": "使用说明",
        "exit": "退出",
        "radius_label": "圆角半径:",
        "color_label": "圆角颜色:",
        "monitors_detected": "检测到 {} 个显示器",
        "anti_burn_in": "防烧屏",
        "anti_burn_in_tip": "启用防止屏幕烧屏",
        "anti_burn_in_interval": "刷新间隔(分钟):",
        "help_title": "使用说明",
        "help_text": (
            "屏幕圆角美化工具\n\n"
            "1. 调整圆角半径滑块可改变圆角大小\n"
            "2. 在托盘菜单中可更改圆角颜色\n"
            "3. 支持多显示器环境\n"
            "4. 如果显示器配置改变，请点击'刷新显示器'\n"
            "5. 启用防烧屏功能防止屏幕损伤\n"
            "6. 可设置开机自动启动\n\n"
            "当前版本: 1.3.1"
        ),
        "black": "纯黑",
        "white": "白色",
        "dark_gray": "深灰",
        "light_gray": "浅灰",
        "dark_blue": "深蓝",
        "dark_green": "深绿",
        "dark_red": "深红",
        "pick_color": "选择颜色...",
        "language": "语言",
        "close": "关闭",
        "minimize": "最小化",
        "restart_required": "需要重启程序以应用语言更改",
        "transparent_mouse": "隐藏圆角区域鼠标",
        "transparent_mouse_tip": "在圆角区域隐藏鼠标光标",
        "close_title": "关闭程序",
        "close_message": "您希望如何操作？",
        "close_exit": "退出程序",
        "close_minimize": "最小化到系统托盘",
        "remember_choice": "记住我的选择"
    },
    "en": {
        "language_name": "English",
        "app_name": "Screen Corner Beautifier",
        "tray_tooltip": "Screen Corner Beautifier",
        "show_main": "Show Main Window",
        "refresh_monitors": "Refresh Monitors",
        "corner_color": "Corner Color",
        "autostart": "Run at Startup",
        "help": "Help",
        "exit": "Exit",
        "radius_label": "Corner Radius:",
        "color_label": "Corner Color:",
        "monitors_detected": "Detected {} monitors",
        "anti_burn_in": "Anti-Burn-in",
        "anti_burn_in_tip": "Enable to prevent screen burn-in",
        "anti_burn_in_interval": "Refresh Interval (min):",
        "help_title": "User Guide",
        "help_text": (
            "Screen Corner Beautifier\n\n"
            "1. Adjust the slider to change corner radius\n"
            "2. Change corner color from tray menu\n"
            "3. Supports multi-monitor setups\n"
            "4. Click 'Refresh Monitors' if display configuration changes\n"
            "5. Enable anti-burn-in to prevent screen damage\n"
            "6. Can be set to run at startup\n\n"
            "Version: 1.3.1"
        ),
        "black": "Black",
        "white": "White",
        "dark_gray": "Dark Gray",
        "light_gray": "Light Gray",
        "dark_blue": "Dark Blue",
        "dark_green": "Dark Green",
        "dark_red": "Dark Red",
        "pick_color": "Pick Color...",
        "language": "Language",
        "close": "Close",
        "minimize": "Minimize",
        "restart_required": "Restart required to apply language changes",
        "transparent_mouse": "Hide mouse in corners",
        "transparent_mouse_tip": "Hide mouse cursor in rounded corner areas",
        "close_title": "Close Program",
        "close_message": "What would you like to do?",
        "close_exit": "Exit Program",
        "close_minimize": "Minimize to System Tray",
        "remember_choice": "Remember my choice"
    },
    "fr": {
        "language_name": "Français",
        "app_name": "Beautificateur de coins d'écran",
        "tray_tooltip": "Beautificateur de coins d'écran",
        "show_main": "Afficher la fenêtre principale",
        "refresh_monitors": "Actualiser les moniteurs",
        "corner_color": "Couleur des coins",
        "autostart": "Démarrer au démarrage",
        "help": "Aide",
        "exit": "Quitter",
        "radius_label": "Rayon des coins:",
        "color_label": "Couleur des coins:",
        "monitors_detected": "{} moniteurs détectés",
        "anti_burn_in": "Anti-Brûlure",
        "anti_burn_in_tip": "Activer pour prévenir la brûlure d'écran",
        "anti_burn_in_interval": "Intervalle de rafraîchissement (min):",
        "help_title": "Guide d'utilisation",
        "help_text": (
            "Beautificateur de coins d'écran\n\n"
            "1. Ajustez le curseur pour changer le rayon des coins\n"
            "2. Changez la couleur des coins depuis le menu de la barre d'état\n"
            "3. Prend en charge les configurations multi-écrans\n"
            "4. Cliquez sur 'Actualiser les moniteurs' si la configuration change\n"
            "5. Activez l'anti-brûlure pour prévenir les dommages à l'écran\n"
            "6. Peut être configuré pour démarrer au démarrage\n\n"
            "Version: 1.3.1"
        ),
        "black": "Noir",
        "white": "Blanc",
        "dark_gray": "Gris foncé",
        "light_gray": "Gris clair",
        "dark_blue": "Bleu foncé",
        "dark_green": "Vert foncé",
        "dark_red": "Rouge foncé",
        "pick_color": "Choisir la couleur...",
        "language": "Langue",
        "close": "Fermer",
        "minimize": "Réduire",
        "restart_required": "Redémarrage requis pour appliquer les changements de langue",
        "transparent_mouse": "Masquer souris dans les coins",
        "transparent_mouse_tip": "Masquer le curseur de la souris dans les zones de coins arrondis",
        "close_title": "Fermer le programme",
        "close_message": "Que souhaitez-vous faire ?",
        "close_exit": "Quitter le programme",
        "close_minimize": "Réduire dans la barre système",
        "remember_choice": "Se souvenir de mon choix"
    },
    "ja": {
        "language_name": "日本語",
        "app_name": "画面コーナー美化ツール",
        "tray_tooltip": "画面コーナー美化ツール",
        "show_main": "メイン画面を表示",
        "refresh_monitors": "モニターを更新",
        "corner_color": "コーナーカラー",
        "autostart": "自動起動",
        "help": "ヘルプ",
        "exit": "終了",
        "radius_label": "コーナー半径:",
        "color_label": "コーナーカラー:",
        "monitors_detected": "{} 台のモニターを検出",
        "anti_burn_in": "焼付防止",
        "anti_burn_in_tip": "焼付防止を有効にする",
        "anti_burn_in_interval": "更新間隔(分):",
        "help_title": "使用説明",
        "help_text": (
            "画面コーナー美化ツール\n\n"
            "1. スライダーでコーナーの半径を調整\n"
            "2. トレイメニューでコーナーカラーを変更\n"
            "3. マルチモニター環境に対応\n"
            "4. モニター構成変更時は「モニターを更新」をクリック\n"
            "5. 焼付防止機能で画面の損傷を防止\n"
            "6. 自動起動を設定可能\n\n"
            "バージョン: 1.3.1"
        ),
        "black": "黒",
        "white": "白",
        "dark_gray": "濃い灰色",
        "light_gray": "薄い灰色",
        "dark_blue": "濃い青",
        "dark_green": "濃い緑",
        "dark_red": "濃い赤",
        "pick_color": "色を選択...",
        "language": "言語",
        "close": "閉じる",
        "minimize": "最小化",
        "restart_required": "言語変更を適用するには再起動が必要です",
        "transparent_mouse": "コーナーでマウスを非表示",
        "transparent_mouse_tip": "角丸領域でマウスカーソルを非表示にする",
        "close_title": "プログラムを閉じる",
        "close_message": "どの操作を実行しますか？",
        "close_exit": "プログラムを終了",
        "close_minimize": "システムトレイに最小化",
        "remember_choice": "選択を記憶"
    },
    "ko": {
        "language_name": "한국어",
        "app_name": "화면 모서리 미화 도구",
        "tray_tooltip": "화면 모서리 미화 도구",
        "show_main": "주 창 표시",
        "refresh_monitors": "모니터 새로 고침",
        "corner_color": "모서리 색상",
        "autostart": "시작 시 실행",
        "help": "도움말",
        "exit": "종료",
        "radius_label": "모서리 반경:",
        "color_label": "모서리 색상:",
        "monitors_detected": "{}개의 모니터 감지됨",
        "anti_burn_in": "번인 방지",
        "anti_burn_in_tip": "번인 방지 활성화",
        "anti_burn_in_interval": "새로 고침 간격(분):",
        "help_title": "사용 설명",
        "help_text": (
            "화면 모서리 미화 도구\n\n"
            "1. 슬라이더로 모서리 반경 조정\n"
            "2. 트레이 메뉴에서 모서리 색상 변경\n"
            "3. 다중 모니터 환경 지원\n"
            "4. 모니터 구성 변경 시 '모니터 새로 고침' 클릭\n"
            "5. 번인 방지 기능으로 화면 손상 방지\n"
            "6. 시작 시 자동 실행 설정 가능\n\n"
            "버전: 1.3.1"
        ),
        "black": "검정",
        "white": "하양",
        "dark_gray": "어두운 회색",
        "light_gray": "밝은 회색",
        "dark_blue": "어두운 파랑",
        "dark_green": "어두운 초록",
        "dark_red": "어두운 빨강",
        "pick_color": "색상 선택...",
        "language": "언어",
        "close": "닫기",
        "minimize": "최소화",
        "restart_required": "언어 변경을 적용하려면 재시작이 필요합니다",
        "transparent_mouse": "코너에서 마우스 숨기기",
        "transparent_mouse_tip": "둥근 모서리 영역에서 마우스 커서 숨기기",
        "close_title": "프로그램 닫기",
        "close_message": "어떤 작업을 실행하시겠습니까?",
        "close_exit": "프로그램 종료",
        "close_minimize": "시스템 트레이로 최소화",
        "remember_choice": "선택 기억"
    }
}

# 获取系统语言
def get_system_language():
    try:
        import locale
        lang = locale.getdefaultlocale()[0]
        if lang:
            lang_code = lang.split('_')[0]
            if lang_code in LANGUAGES:
                return lang_code
    except:
        pass
    return "en"

# 当前语言
CURRENT_LANG = get_system_language()
tr = lambda text: LANGUAGES[CURRENT_LANG].get(text, text)

class CornerWindow(QtWidgets.QWidget):
    def __init__(self, screen, position: str, radius: int, color: QtGui.QColor, 
                 anti_burn_in=False, hide_mouse=False):
        super().__init__()
        self.screen = screen
        self.position = position
        self.radius = radius
        self.color = color
        self.anti_burn_in = anti_burn_in
        self.hide_mouse = hide_mouse
        self.original_pos = None
        self.last_move_time = time.time()
        self.hwnd = None  # 存储窗口句柄

        # Windows 兼容性设置
        if sys.platform == "win32":
            try:
                self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
                self.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground, True)
            except:
                pass
            
        # 修改窗口标志
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint |
            QtCore.Qt.WindowType.Tool |
            QtCore.Qt.WindowType.BypassWindowManagerHint |
            QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        
        # 设置更高的Z序以确保在任务栏前
        self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, True)
        
        # 设置鼠标隐藏
        if self.hide_mouse:
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.BlankCursor))
        
        self.update_geometry()

        # 防烧屏定时器
        self.burn_in_timer = QtCore.QTimer(self)
        self.burn_in_timer.timeout.connect(self.anti_burn_in_update)
        if self.anti_burn_in:
            self.burn_in_timer.start(60 * 1000)  # 每分钟检查一次
            
        # 置顶检查定时器
        self.topmost_timer = QtCore.QTimer(self)
        self.topmost_timer.timeout.connect(self.ensure_topmost)
        self.topmost_timer.start(1000)  # 每秒检查一次置顶状态
        
        # 窗口显示后获取句柄
        self.showEvent = self.on_show_event

    def on_show_event(self, event):
        """窗口显示时获取句柄并强制置顶"""
        super().showEvent(event)
        self.hwnd = int(self.winId())
        self.force_topmost()
        
    def force_topmost(self):
        """强制窗口置于最顶层"""
        if not self.hwnd:
            return
            
        try:
            # 设置窗口为最顶层
            ctypes.windll.user32.SetWindowPos(
                self.hwnd, 
                -1,  # HWND_TOPMOST
                0, 0, 0, 0,
                0x0001 | 0x0002 | 0x0010  # SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE
            )
            
            # 设置窗口为系统覆盖窗口
            ex_style = ctypes.windll.user32.GetWindowLongW(self.hwnd, -20)  # GWL_EXSTYLE
            ex_style |= 0x00000008  # WS_EX_TOPMOST
            ex_style |= 0x00000080  # WS_EX_TOOLWINDOW
            ex_style |= 0x00000020  # WS_EX_TRANSPARENT (允许鼠标穿透)
            ctypes.windll.user32.SetWindowLongW(self.hwnd, -20, ex_style)
            
            # 再次确认置顶
            ctypes.windll.user32.SetWindowPos(
                self.hwnd, 
                -1,  # HWND_TOPMOST
                0, 0, 0, 0,
                0x0001 | 0x0002 | 0x0010  # SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE
            )
        except Exception as e:
            print(f"强制置顶失败: {e}")

    def ensure_topmost(self):
        """确保窗口始终位于最顶层"""
        if not self.isVisible() or not self.hwnd:
            return
            
        try:
            # 检查窗口是否在最顶层
            top_window = ctypes.windll.user32.GetTopWindow(0)
            if top_window != self.hwnd:
                self.force_topmost()
        except:
            pass

    def update_geometry(self):
        screen_geo = self.screen.geometry()
        r = self.radius
        
        # 考虑DPI缩放
        dpi_scale = self.screen.devicePixelRatio()
        scaled_r = int(r * dpi_scale)
        
        if self.position == 'tl':
            self.setGeometry(screen_geo.x(), screen_geo.y(), scaled_r, scaled_r)
            self.original_pos = (screen_geo.x(), screen_geo.y())
        elif self.position == 'tr':
            self.setGeometry(screen_geo.x() + screen_geo.width() - scaled_r, 
                             screen_geo.y(), scaled_r, scaled_r)
            self.original_pos = (screen_geo.x() + screen_geo.width() - scaled_r, screen_geo.y())
        elif self.position == 'bl':
            self.setGeometry(screen_geo.x(), 
                             screen_geo.y() + screen_geo.height() - scaled_r, 
                             scaled_r, scaled_r)
            self.original_pos = (screen_geo.x(), screen_geo.y() + screen_geo.height() - scaled_r)
        elif self.position == 'br':
            self.setGeometry(screen_geo.x() + screen_geo.width() - scaled_r, 
                             screen_geo.y() + screen_geo.height() - scaled_r, 
                             scaled_r, scaled_r)
            self.original_pos = (screen_geo.x() + screen_geo.width() - scaled_r, 
                                 screen_geo.y() + screen_geo.height() - scaled_r)
        self.update()

    def paintEvent(self, event):
        r = self.width()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(self.color)
        painter.drawRect(0, 0, r, r)
        
        path = QtGui.QPainterPath()
        if self.position == 'tl':
            path.addEllipse(0, 0, 2*r, 2*r)
        elif self.position == 'tr':
            path.addEllipse(-r, 0, 2*r, 2*r)
        elif self.position == 'bl':
            path.addEllipse(0, -r, 2*r, 2*r)
        elif self.position == 'br':
            path.addEllipse(-r, -r, 2*r, 2*r)
        
        painter.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_Clear)
        painter.drawPath(path)

    def anti_burn_in_update(self):
        if not self.anti_burn_in:
            return
            
        current_time = time.time()
        # 每5分钟微移一次位置
        if current_time - self.last_move_time > 300:
            dx = random.randint(-2, 2)
            dy = random.randint(-2, 2)
            self.move(self.x() + dx, self.y() + dy)
            self.last_move_time = current_time
            
        # 每60分钟重置位置
        if current_time - self.last_move_time > 3600:
            self.reset_position()
            self.last_move_time = current_time

    def reset_position(self):
        if self.original_pos:
            self.move(self.original_pos[0], self.original_pos[1])
            self.update()
            
    def winEvent(self, event):
        """处理Windows消息"""
        if event.message == 0x0046:  # WM_WINDOWPOSCHANGING
            # 防止窗口位置被改变
            return True
        return super().winEvent(event)


class TrayApp(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.setToolTip(tr("tray_tooltip"))
        self.parent = parent
        self.menu = QtWidgets.QMenu(parent)
        self.setContextMenu(self.menu)
        
        # 连接双击事件
        self.activated.connect(self.on_tray_activated)
        
        self.create_menu()
        
    def on_tray_activated(self, reason):
        # 双击托盘图标打开主界面
        if reason == QtWidgets.QSystemTrayIcon.ActivationReason.DoubleClick:
            self.parent.show_main_window()
        
    def create_menu(self):
        self.menu.clear()
        
        # 显示主界面
        self.show_action = self.menu.addAction(tr("show_main"))
        self.show_action.triggered.connect(self.parent.show_main_window)
        
        # 刷新显示器按钮
        refresh_action = self.menu.addAction(tr("refresh_monitors"))
        refresh_action.triggered.connect(self.parent.refresh_corners)
        
        # 圆角颜色菜单
        color_menu = self.menu.addMenu(tr("corner_color"))
        self.color_actions = {}
        colors = {
            tr("black"): QtGui.QColor(0, 0, 0),
            tr("white"): QtGui.QColor(255, 255, 255),
            tr("dark_gray"): QtGui.QColor(40, 40, 40),
            tr("light_gray"): QtGui.QColor(200, 200, 200),
            tr("dark_blue"): QtGui.QColor(0, 0, 80),
            tr("dark_green"): QtGui.QColor(0, 60, 0),
            tr("dark_red"): QtGui.QColor(80, 0, 0)
        }
        for name, color in colors.items():
            action = color_menu.addAction(name)
            action.setData(color)
            action.triggered.connect(lambda checked, c=color: self.parent.update_color(c))
            self.color_actions[name] = action
        
        # 语言选择菜单
        lang_menu = self.menu.addMenu(tr("language"))
        self.lang_actions = {}
        
        # 先添加中文
        zh_action = lang_menu.addAction(LANGUAGES["zh"]["language_name"])
        zh_action.setData("zh")
        zh_action.triggered.connect(self.change_language)
        self.lang_actions["zh"] = zh_action
        if "zh" == CURRENT_LANG:
            zh_action.setCheckable(True)
            zh_action.setChecked(True)
        
        # 添加其他语言
        for lang_code, lang_data in LANGUAGES.items():
            if lang_code == "zh":
                continue
            action = lang_menu.addAction(lang_data["language_name"])
            action.setData(lang_code)
            action.triggered.connect(self.change_language)
            self.lang_actions[lang_code] = action
            if lang_code == CURRENT_LANG:
                action.setCheckable(True)
                action.setChecked(True)
        
        # 添加分隔线
        lang_menu.addSeparator()
        
        # 开机启动
        self.startup_action = self.menu.addAction(tr("autostart"))
        self.startup_action.setCheckable(True)
        self.startup_action.setChecked(self.is_auto_start_enabled())
        self.startup_action.triggered.connect(self.toggle_auto_start)
        
        # 帮助菜单
        help_action = self.menu.addAction(tr("help"))
        help_action.triggered.connect(self.show_help)

        # 退出
        exit_action = self.menu.addAction(tr("exit"))
        exit_action.triggered.connect(self.quit_application)

    def quit_application(self):
        self.parent.save_config()
        QtWidgets.QApplication.quit()
        
    def change_language(self):
        action = self.sender()
        lang_code = action.data()
        global CURRENT_LANG
        CURRENT_LANG = lang_code
        
        # 保存语言设置
        try:
            config = {}
            if os.path.exists(CONFIG_PATH):
                with open(CONFIG_PATH, 'r') as f:
                    config = json.load(f)
            config['language'] = lang_code
            with open(CONFIG_PATH, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            print(f"保存语言配置失败: {e}")
        
        # 重新创建菜单
        self.create_menu()
        
        # 更新主窗口内容
        self.parent.update_ui_language()
        
        # 提示用户需要重启
        # 已移除重启提示，因为现在支持动态切换

    def toggle_auto_start(self):
        if self.startup_action.isChecked():
            self.enable_auto_start()
        else:
            self.disable_auto_start()

    def enable_auto_start(self):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        exe_path = sys.executable
        if getattr(sys, 'frozen', False):
            script_path = sys.executable
        else:
            script_path = os.path.abspath(__file__)
        cmd = f'"{exe_path}" "{script_path}"'
        winreg.SetValueEx(key, "RoundedCorners", 0, winreg.REG_SZ, cmd)
        winreg.CloseKey(key)

    def disable_auto_start(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, "RoundedCorners")
            winreg.CloseKey(key)
        except FileNotFoundError:
            pass

    def is_auto_start_enabled(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Run")
            value, _ = winreg.QueryValueEx(key, "RoundedCorners")
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            return False
            
    def show_help(self):
        help_dialog = QtWidgets.QMessageBox()
        help_dialog.setWindowTitle(tr("help_title"))
        help_dialog.setText(tr("help_text"))
        help_dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)
        help_dialog.exec()


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr("app_name"))
        self.setFixedSize(500, 350)  # 增加窗口高度以适应新布局
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 主容器
        self.container = QtWidgets.QFrame()
        self.container.setObjectName("mainContainer")
        self.container_layout = QtWidgets.QVBoxLayout(self.container)
        
        # 增加容器内边距，特别是左右边距
        self.container_layout.setContentsMargins(20, 15, 20, 15)  # 左右边距增加到20px
        self.container_layout.setSpacing(15)
        
        # 圆角半径设置
        self.radius_layout = QtWidgets.QHBoxLayout()
        
        # 为标签添加边距
        self.radius_label = QtWidgets.QLabel(tr("radius_label"))
        self.radius_label.setContentsMargins(8, 0, 8, 0)  # 添加左右边距（约一个空格字符）
        self.radius_layout.addWidget(self.radius_label)
        
        self.radius_spin = QtWidgets.QSpinBox()
        self.radius_spin.setRange(1, 50)
        self.radius_spin.setValue(20)
        self.radius_spin.setObjectName("radiusSpin")
        self.radius_layout.addWidget(self.radius_spin)
        
        self.radius_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.radius_slider.setRange(1, 50)
        self.radius_slider.setValue(20)
        self.radius_slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.radius_slider.setTickInterval(5)
        self.radius_slider.setObjectName("radiusSlider")
        self.radius_layout.addWidget(self.radius_slider, 4)
        
        self.container_layout.addLayout(self.radius_layout)
        
        # 颜色设置
        self.color_layout = QtWidgets.QHBoxLayout()
        
        # 为标签添加边距
        self.color_label = QtWidgets.QLabel(tr("color_label"))
        self.color_label.setContentsMargins(8, 0, 8, 0)  # 添加左右边距（约一个空格字符）
        self.color_layout.addWidget(self.color_label)
        
        self.color_preview = QtWidgets.QFrame()
        self.color_preview.setFixedSize(32, 32)
        self.color_preview.setObjectName("colorPreview")
        self.color_layout.addWidget(self.color_preview)
        
        # 添加三个预设颜色按钮
        self.preset_colors_layout = QtWidgets.QHBoxLayout()
        self.preset_colors_layout.setSpacing(5)
        
        # 黑色按钮
        self.black_btn = QtWidgets.QPushButton()
        self.black_btn.setFixedSize(32, 32)
        self.black_btn.setStyleSheet("background-color: #000000; border-radius: 4px;")
        self.black_btn.clicked.connect(lambda: self.update_color(QtGui.QColor(0, 0, 0)))
        self.preset_colors_layout.addWidget(self.black_btn)
        
        # 深灰色按钮
        self.dark_gray_btn = QtWidgets.QPushButton()
        self.dark_gray_btn.setFixedSize(32, 32)
        self.dark_gray_btn.setStyleSheet("background-color: #282828; border-radius: 4px;")
        self.dark_gray_btn.clicked.connect(lambda: self.update_color(QtGui.QColor(40, 40, 40)))
        self.preset_colors_layout.addWidget(self.dark_gray_btn)
        
        # 浅灰色按钮
        self.light_gray_btn = QtWidgets.QPushButton()
        self.light_gray_btn.setFixedSize(32, 32)
        self.light_gray_btn.setStyleSheet("background-color: #C8C8C8; border-radius: 4px;")
        self.light_gray_btn.clicked.connect(lambda: self.update_color(QtGui.QColor(200, 200, 200)))
        self.preset_colors_layout.addWidget(self.light_gray_btn)
        
        self.color_layout.addLayout(self.preset_colors_layout)
        
        # 颜色选择按钮
        self.color_btn = QtWidgets.QPushButton(tr("pick_color"))
        self.color_btn.setFixedSize(120, 32)
        self.color_btn.setObjectName("colorButton")
        self.color_btn.clicked.connect(self.pick_color)
        self.color_layout.addWidget(self.color_btn)
        
        self.color_layout.addStretch()
        self.container_layout.addLayout(self.color_layout)
        
        # 防烧屏设置
        self.anti_burn_layout = QtWidgets.QHBoxLayout()
        
        self.anti_burn_in_check = QtWidgets.QCheckBox(tr("anti_burn_in"))
        self.anti_burn_in_check.setToolTip(tr("anti_burn_in_tip"))
        self.anti_burn_in_check.setObjectName("antiBurnCheck")
        self.anti_burn_layout.addWidget(self.anti_burn_in_check)
        
        # 刷新间隔标签和输入框
        self.anti_burn_interval_label = QtWidgets.QLabel(tr("anti_burn_in_interval"))
        self.anti_burn_interval_label.setContentsMargins(8, 0, 8, 0)  # 添加左右边距（约一个空格字符）
        self.anti_burn_layout.addWidget(self.anti_burn_interval_label)
        
        self.anti_burn_in_interval = QtWidgets.QSpinBox()
        self.anti_burn_in_interval.setRange(1, 120)
        self.anti_burn_in_interval.setValue(10)
        self.anti_burn_in_interval.setFixedWidth(70)
        self.anti_burn_in_interval.setObjectName("antiBurnInterval")
        self.anti_burn_layout.addWidget(self.anti_burn_in_interval)
        
        self.anti_burn_layout.addStretch()
        self.container_layout.addLayout(self.anti_burn_layout)
        
        # 隐藏鼠标设置
        self.mouse_layout = QtWidgets.QHBoxLayout()
        
        self.transparent_mouse_check = QtWidgets.QCheckBox(tr("transparent_mouse"))
        self.transparent_mouse_check.setToolTip(tr("transparent_mouse_tip"))
        self.transparent_mouse_check.setObjectName("transparentMouseCheck")
        self.transparent_mouse_check.setContentsMargins(8, 0, 8, 0)  # 添加左右边距（约一个空格字符）
        self.mouse_layout.addWidget(self.transparent_mouse_check)
        
        self.mouse_layout.addStretch()
        self.container_layout.addLayout(self.mouse_layout)
        
        # 显示器信息
        self.monitor_label = QtWidgets.QLabel(tr("monitors_detected").format(1))
        self.monitor_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.monitor_label.setObjectName("monitorLabel")
        self.container_layout.addWidget(self.monitor_label)
        
        layout.addWidget(self.container)
        
        # 初始化圆角窗口列表
        self.corners = []
        self.corner_color = QtGui.QColor(0, 0, 0)
        self.anti_burn_in_enabled = False
        self.transparent_mouse_enabled = False
        
        # 获取当前主题
        self.current_theme = self.get_system_theme()
        
        # 加载配置
        self.load_config()
        
        # 创建圆角窗口
        self.refresh_corners()
        
        # 连接信号
        self.radius_spin.valueChanged.connect(self.update_radius)
        self.radius_slider.valueChanged.connect(self.radius_spin.setValue)
        self.radius_slider.valueChanged.connect(self.update_radius)
        self.anti_burn_in_check.stateChanged.connect(self.toggle_anti_burn_in)
        self.anti_burn_in_interval.valueChanged.connect(self.update_burn_in_interval)
        self.transparent_mouse_check.stateChanged.connect(self.toggle_transparent_mouse)
        
        # 监听显示器变化
        app = QtWidgets.QApplication.instance()
        app.screenAdded.connect(self.handle_screen_change)
        app.screenRemoved.connect(self.handle_screen_change)
        
        # 应用样式
        self.apply_theme()
        
        # 监听主题变化
        self.theme_timer = QtCore.QTimer(self)
        self.theme_timer.timeout.connect(self.check_theme_change)
        self.theme_timer.start(10000)  # 每10秒检查一次主题变化，减少频率
        
        # 添加任务栏状态监听
        self.taskbar_timer = QtCore.QTimer(self)
        self.taskbar_timer.timeout.connect(self.check_taskbar_state)
        self.taskbar_timer.start(2000)  # 每2秒检查一次任务栏状态
        
        # 添加窗口刷新定时器
        self.refresh_timer = QtCore.QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_corners)
        self.refresh_timer.start(5000)  # 每5秒刷新一次窗口位置
        
        # 关闭行为记忆
        self.close_action = None
    
    def show_main_window(self):
        """显示主窗口并激活"""
        self.show()
        self.activateWindow()
        self.raise_()
    
    def update_ui_language(self):
        """更新界面语言"""
        # 更新窗口标题
        self.setWindowTitle(tr("app_name"))
        
        # 更新所有标签文本
        self.radius_label.setText(tr("radius_label"))
        self.color_label.setText(tr("color_label"))
        self.anti_burn_in_check.setText(tr("anti_burn_in"))
        self.anti_burn_in_check.setToolTip(tr("anti_burn_in_tip"))
        self.anti_burn_interval_label.setText(tr("anti_burn_in_interval"))
        self.transparent_mouse_check.setText(tr("transparent_mouse"))
        self.transparent_mouse_check.setToolTip(tr("transparent_mouse_tip"))
        self.color_btn.setText(tr("pick_color"))
        
        # 更新显示器数量显示
        screens = QtWidgets.QApplication.screens()
        self.monitor_label.setText(tr("monitors_detected").format(len(screens)))
        
        # 重新应用样式
        self.apply_theme()
    
    def get_icon_path(self):
        # 优先查找当前目录下的icon.ico
        paths_to_try = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "icon.ico"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "icon.png"),
            os.path.join(os.path.dirname(sys.executable), "icon.ico"),
            os.path.join(os.path.dirname(sys.executable), "icon.png"),
            os.path.join(os.path.dirname(sys.executable), "resources", "icon.ico"),
            os.path.join(os.path.dirname(sys.executable), "resources", "icon.png")
        ]
        
        for path in paths_to_try:
            if os.path.exists(path):
                return path
        return ""
    
    def get_system_theme(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            return "light" if value == 1 else "dark"
        except:
            return "light"
    
    def check_theme_change(self):
        new_theme = self.get_system_theme()
        if new_theme != self.current_theme:
            self.current_theme = new_theme
            self.apply_theme()
    
    def check_taskbar_state(self):
        """检查任务栏位置是否变化"""
        try:
            # 使用Windows API获取任务栏位置
            appbar_data = ctypes.windll.shell32.APPBARDATA()
            appbar_data.cbSize = ctypes.sizeof(appbar_data)
            if ctypes.windll.shell32.SHAppBarMessage(4, ctypes.byref(appbar_data)):  # ABM_GETTASKBARPOS
                # 如果任务栏位置发生变化，刷新圆角
                current_pos = (appbar_data.rc.left, appbar_data.rc.top, 
                              appbar_data.rc.right, appbar_data.rc.bottom)
                if hasattr(self, 'last_taskbar_pos') and current_pos != self.last_taskbar_pos:
                    self.refresh_corners()
                self.last_taskbar_pos = current_pos
        except:
            pass
    
    def apply_theme(self):
        # 设置窗口图标
        icon_path = self.get_icon_path()
        if icon_path and os.path.exists(icon_path):
            self.setWindowIcon(QtGui.QIcon(icon_path))
        
        if self.current_theme == "dark":
            # 深色主题
            self.setStyleSheet("""
                QWidget {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    font-family: "Segoe UI", "Microsoft YaHei";
                }
                #mainContainer {
                    background-color: #333333;
                    border-radius: 8px;
                    border: 1px solid #444444;
                    padding: 15px;
                }
                QLabel {
                    color: #e0e0e0;
                    font-size: 10pt;
                }
                QSpinBox, QPushButton, QComboBox {
                    background-color: #444444;
                    color: #e0e0e0;
                    border: 1px solid #555555;
                    border-radius: 4px;
                    padding: 6px;
                    font-size: 10pt;
                }
                QSpinBox:hover, QPushButton:hover, QComboBox:hover {
                    background-color: #555555;
                }
                QSpinBox:focus, QPushButton:pressed, QComboBox:on {
                    background-color: #666666;
                }
                #radiusSlider::groove:horizontal {
                    height: 6px;
                    background: #555555;
                    border-radius: 3px;
                }
                #radiusSlider::handle:horizontal {
                    background: #4a9cff;
                    width: 16px;
                    height: 16px;
                    margin: -5px 0;
                    border-radius: 8px;
                }
                #radiusSlider::sub-page:horizontal {
                    background: #4a9cff;
                    border-radius: 3px;
                }
                QCheckBox {
                    color: #e0e0e0;
                    font-size: 10pt;
                }
                #monitorLabel {
                    color: #aaaaaa;
                    font-size: 9pt;
                    margin-top: 10px;
                }
            """)
        else:
            # 浅色主题
            self.setStyleSheet("""
                QWidget {
                    background-color: #f5f5f5;
                    color: #333333;
                    font-family: "Segoe UI", "Microsoft YaHei";
                }
                #mainContainer {
                    background-color: #ffffff;
                    border-radius: 8px;
                    border: 1px solid #e0e0e0;
                    padding: 15px;
                }
                QLabel {
                    color: #333333;
                    font-size: 10pt;
                }
                QSpinBox, QPushButton, QComboBox {
                    background-color: #ffffff;
                    color: #333333;
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                    padding: 6px;
                    font-size: 10pt;
                }
                QSpinBox:hover, QPushButton:hover, QComboBox:hover {
                    background-color: #f0f0f0;
                }
                QSpinBox:focus, QPushButton:pressed, QComboBox:on {
                    background-color: #e0e0e0;
                }
                #radiusSlider::groove:horizontal {
                    height: 6px;
                    background: #d7d7d7;
                    border-radius: 3px;
                }
                #radiusSlider::handle:horizontal {
                    background: #4a9cff;
                    width: 16px;
                    height: 16px;
                    margin: -5px 0;
                    border-radius: 8px;
                }
                #radiusSlider::sub-page:horizontal {
                    background: #4a9cff;
                    border-radius: 3px;
                }
                QCheckBox {
                    color: #333333;
                    font-size: 10pt;
                }
                #monitorLabel {
                    color: #666666;
                    font-size: 9pt;
                    margin-top: 10px;
                }
            """)
        
        # 更新颜色预览
        self.update_color_preview()
    
    def load_config(self):
        try:
            if os.path.exists(CONFIG_PATH):
                with open(CONFIG_PATH, 'r') as f:
                    config = json.load(f)
                    self.radius_spin.setValue(config.get('radius', 20))
                    color = config.get('color', [0, 0, 0])
                    self.corner_color = QtGui.QColor(*color)
                    self.update_color_preview()
                    self.anti_burn_in_enabled = config.get('anti_burn_in', False)
                    self.anti_burn_in_check.setChecked(self.anti_burn_in_enabled)
                    self.anti_burn_in_interval.setValue(config.get('burn_in_interval', 10))
                    self.transparent_mouse_enabled = config.get('transparent_mouse', False)
                    self.transparent_mouse_check.setChecked(self.transparent_mouse_enabled)
                    self.close_action = config.get('close_action')
                    
                    # 加载语言设置
                    lang = config.get('language')
                    if lang and lang in LANGUAGES:
                        global CURRENT_LANG
                        CURRENT_LANG = lang
        except Exception as e:
            print(f"加载配置失败: {e}")
    
    def save_config(self):
        try:
            config = {
                'radius': self.radius_spin.value(),
                'color': [self.corner_color.red(), 
                         self.corner_color.green(), 
                         self.corner_color.blue()],
                'anti_burn_in': self.anti_burn_in_enabled,
                'burn_in_interval': self.anti_burn_in_interval.value(),
                'transparent_mouse': self.transparent_mouse_enabled,
                'language': CURRENT_LANG,
                'close_action': self.close_action
            }
            with open(CONFIG_PATH, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def update_radius(self, val):
        for w in self.corners:
            w.radius = val
            w.update_geometry()
        self.save_config()
    
    def update_color(self, color):
        self.corner_color = color
        for w in self.corners:
            w.color = color
            w.update()
        self.update_color_preview()
        self.save_config()
    
    def update_color_preview(self):
        border_color = "#cccccc" if self.current_theme == "light" else "#555555"
        self.color_preview.setStyleSheet(
            f"background-color: {self.corner_color.name()}; "
            f"border-radius: 4px; border: 1px solid {border_color};"
        )
    
    def pick_color(self):
        color = QtWidgets.QColorDialog.getColor(self.corner_color, self, tr("pick_color"))
        if color.isValid():
            self.update_color(color)
    
    def toggle_anti_burn_in(self, state):
        self.anti_burn_in_enabled = state == QtCore.Qt.CheckState.Checked.value
        for w in self.corners:
            w.anti_burn_in = self.anti_burn_in_enabled
            if self.anti_burn_in_enabled:
                w.burn_in_timer.start(self.anti_burn_in_interval.value() * 60 * 1000)
            else:
                w.burn_in_timer.stop()
                w.reset_position()
        self.save_config()
    
    def toggle_transparent_mouse(self, state):
        self.transparent_mouse_enabled = state == QtCore.Qt.CheckState.Checked.value
        for w in self.corners:
            w.hide_mouse = self.transparent_mouse_enabled
            if self.transparent_mouse_enabled:
                w.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.BlankCursor))
            else:
                w.unsetCursor()
        self.save_config()
    
    def update_burn_in_interval(self, value):
        # 更新所有窗口的定时器间隔
        for w in self.corners:
            if w.anti_burn_in:
                w.burn_in_timer.stop()
                w.burn_in_timer.start(value * 60 * 1000)
        self.save_config()
    
    def refresh_corners(self):
        """刷新圆角窗口，确保正确位置和层级"""
        # 清除现有圆角
        for w in self.corners:
            w.close()
            w.deleteLater()
        self.corners.clear()
        
        # 创建所有显示器的圆角
        screens = QtWidgets.QApplication.screens()
        self.monitor_label.setText(tr("monitors_detected").format(len(screens)))
        
        for screen in screens:
            for pos in ['tl', 'tr', 'bl', 'br']:
                w = CornerWindow(screen, pos, self.radius_spin.value(), 
                                self.corner_color, self.anti_burn_in_enabled,
                                self.transparent_mouse_enabled)
                w.show()
                
                # 强制窗口显示在最前面
                w.raise_()
                w.activateWindow()
                
                self.corners.append(w)
        
        # 延迟确保所有窗口创建完成
        QtCore.QTimer.singleShot(100, self.force_all_topmost)
        
    def force_all_topmost(self):
        """强制所有圆角窗口置顶"""
        for w in self.corners:
            if hasattr(w, 'hwnd') and w.hwnd:
                try:
                    # 设置窗口为最顶层
                    ctypes.windll.user32.SetWindowPos(
                        w.hwnd, 
                        -1,  # HWND_TOPMOST
                        0, 0, 0, 0,
                        0x0001 | 0x0002 | 0x0010  # SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE
                    )
                except:
                    pass
    
    def handle_screen_change(self):
        """处理屏幕变化事件"""
        # 延迟执行以确保屏幕信息已更新
        QtCore.QTimer.singleShot(1000, self.refresh_corners)
    
    def closeEvent(self, event):
        # 如果有记忆的关闭行为，直接执行
        if self.close_action is not None:
            if self.close_action == 0:
                self.save_config()
                QtWidgets.QApplication.quit()
            else:
                event.ignore()
                self.hide()
            return
        
        # 创建关闭对话框
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(tr("close_title"))
        dialog.setFixedSize(350, 150)
        
        layout = QtWidgets.QVBoxLayout(dialog)
        
        # 提示信息
        label = QtWidgets.QLabel(tr("close_message"))
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        # 按钮布局
        btn_layout = QtWidgets.QHBoxLayout()
        
        # 用户选择的动作
        user_action = [None]  # 使用列表以便在闭包中修改
        
        def set_action_and_accept(action_value):
            user_action[0] = action_value
            dialog.accept()
        
        exit_btn = QtWidgets.QPushButton(tr("close_exit"))
        exit_btn.clicked.connect(lambda: set_action_and_accept(0))
        btn_layout.addWidget(exit_btn)
        
        minimize_btn = QtWidgets.QPushButton(tr("close_minimize"))
        minimize_btn.clicked.connect(lambda: set_action_and_accept(1))
        btn_layout.addWidget(minimize_btn)
        
        layout.addLayout(btn_layout)
        
        # 记住选择复选框
        remember_check = QtWidgets.QCheckBox(tr("remember_choice"))
        remember_check.setChecked(False)
        layout.addWidget(remember_check, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        
        # 显示对话框并等待用户选择
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            if remember_check.isChecked() and user_action[0] is not None:
                self.close_action = user_action[0]
                self.save_config()
            
            # 执行用户选择的动作
            if user_action[0] == 0:
                self.save_config()
                QtWidgets.QApplication.quit()
            elif user_action[0] == 1:
                event.ignore()
                self.hide()
        else:
            event.ignore()
    
    def handle_close_action(self, action, dialog):
        self.close_action = action
        self.save_config()
        
        if action == 0:
            QtWidgets.QApplication.quit()
        else:
            self.hide()
            dialog.accept()


def main():
    # 检查是否已存在实例
    if last_error == 183:  # ERROR_ALREADY_EXISTS
        sys.exit(1)
        
    app = QtWidgets.QApplication(sys.argv)
    
    # 设置Windows 11风格
    if sys.platform == "win32":
        os_version = platform.release()
        if os_version and int(os_version) >= 10:
            app.setStyle("Fusion")
    
    # 创建主窗口
    window = MainWindow()
    
    # 创建托盘图标
    icon_path = window.get_icon_path()
    if icon_path and os.path.exists(icon_path):
        icon = QtGui.QIcon(icon_path)
    else:
        # 创建默认图标
        pixmap = QtGui.QPixmap(32, 32)
        pixmap.fill(QtGui.QColor(0, 0, 0, 0))
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setBrush(QtGui.QColor(100, 100, 255))
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(4, 4, 24, 24, 8, 8)
        painter.end()
        icon = QtGui.QIcon(pixmap)
    
    tray_icon = TrayApp(icon, window)
    window.tray_icon = tray_icon

    tray_icon.show()
    window.show_main_window()  # 使用新方法显示主窗口
    
    # 设置当最后一个窗口关闭时不退出应用程序
    app.setQuitOnLastWindowClosed(False)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()