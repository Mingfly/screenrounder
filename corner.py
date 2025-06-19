# corner.py
import sys
import ctypes
import time
import random
from PyQt6 import QtWidgets, QtCore, QtGui

class CornerWindow(QtWidgets.QWidget):
    def __init__(self, screen, position: str, radius: int, color: QtGui.QColor,
                 anti_burn_in=False, hide_mouse=False, burn_in_interval=10):
        super().__init__()
        self.screen = screen
        self.position = position
        self.radius = radius
        self.color = color
        self.anti_burn_in = anti_burn_in
        self.hide_mouse = hide_mouse
        self.burn_in_interval = burn_in_interval  # 分钟
        self.original_pos = None
        self.last_move_time = time.time()
        self.last_reset_time = time.time()

        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint |
            QtCore.Qt.WindowType.Tool |
            QtCore.Qt.WindowType.BypassWindowManagerHint |
            QtCore.Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        if self.hide_mouse:
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.BlankCursor))

        self.update_geometry()
        self.set_topmost()

        # 优化：减少定时器频率
        self.topmost_timer = QtCore.QTimer(self)
        self.topmost_timer.timeout.connect(self.ensure_topmost)
        self.topmost_timer.start(5000)  # 每5秒而非1秒

        # 仅在需要时创建防烧屏定时器
        self.burn_in_timer = None
        if self.anti_burn_in:
            self.create_burn_in_timer()
    
    def create_burn_in_timer(self):
        """仅在需要时创建防烧屏定时器"""
        if self.burn_in_timer is None:
            self.burn_in_timer = QtCore.QTimer(self)
            self.burn_in_timer.timeout.connect(self.anti_burn_in_update)
            self.start_anti_burn_in_timer()

    def set_topmost(self):
        """使用Windows API强制窗口置顶"""
        if sys.platform == "win32":
            try:
                hwnd = self.winId().__int__()
                ctypes.windll.user32.SetWindowPos(
                    hwnd, -1, 0, 0, 0, 0,
                    0x0001 | 0x0002 | 0x0010  # SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE
                )
            except Exception as e:
                print("设置置顶失败:", e)

    def ensure_topmost(self):
        if not self.isActiveWindow():
            self.raise_()

    def update_geometry(self):
        geo = self.screen.geometry()
        dpi_scale = self.screen.devicePixelRatio()
        r = int(self.radius * dpi_scale)

        if self.position == 'tl':
            self.setGeometry(geo.x(), geo.y(), r, r)
            self.original_pos = (geo.x(), geo.y())
        elif self.position == 'tr':
            self.setGeometry(geo.x() + geo.width() - r, geo.y(), r, r)
            self.original_pos = (geo.x() + geo.width() - r, geo.y())
        elif self.position == 'bl':
            self.setGeometry(geo.x(), geo.y() + geo.height() - r, r, r)
            self.original_pos = (geo.x(), geo.y() + geo.height() - r)
        elif self.position == 'br':
            self.setGeometry(geo.x() + geo.width() - r, geo.y() + geo.height() - r, r, r)
            self.original_pos = (geo.x() + geo.width() - r, geo.y() + geo.height() - r)

        self.ensure_topmost()
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
        if not self.anti_burn_in or not self.burn_in_timer:
            return
        now = time.time()
        if now - self.last_move_time > self.burn_in_interval * 60:
            dx = random.randint(-1, 1)
            dy = random.randint(-1, 1)
            self.move(self.x() + dx, self.y() + dy)
            self.last_move_time = now
        if now - self.last_reset_time > 3600:
            self.reset_position()
            self.last_reset_time = now

    def start_anti_burn_in_timer(self):
        if self.anti_burn_in and self.burn_in_timer:
            self.burn_in_timer.start(self.burn_in_interval * 60 * 1000)

    def update_burn_in_interval(self, interval):
        self.burn_in_interval = interval
        if self.anti_burn_in and self.burn_in_timer:
            self.burn_in_timer.stop()
            self.start_anti_burn_in_timer()

    def reset_position(self):
        """重置窗口到原始位置"""
        if self.original_pos:
            self.move(*self.original_pos)
            # 重置防烧屏计时器
            self.last_move_time = time.time()
            self.last_reset_time = time.time()
            self.update()
            self.ensure_topmost()
    
    def close(self):
        """重写close方法以释放资源"""
        if self.topmost_timer and self.topmost_timer.isActive():
            self.topmost_timer.stop()
        if self.burn_in_timer and self.burn_in_timer.isActive():
            self.burn_in_timer.stop()
        super().close()
