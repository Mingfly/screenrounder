#main_window.py
import sys
import os
from PyQt6 import QtWidgets, QtGui, QtCore
from corner import CornerWindow
from config import load_config, save_config
from utils import get_system_theme, get_icon_path
from language import tr, set_language, CURRENT_LANG
from signals import language_signal  # 导入全局语言信号

CANDIDATE_COLORS = {
    "black": QtGui.QColor(0, 0, 0),
    "white": QtGui.QColor(255, 255, 255),
    "dark_gray": QtGui.QColor(80, 80, 80),
    "light_gray": QtGui.QColor(200, 200, 200),
    "dark_blue": QtGui.QColor(0, 0, 128)
}

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr("app_name"))
        self.setFixedSize(500, 300)
        
        # 设置窗口标志以支持深色模式
        if sys.platform == "win32":
            # Windows 系统
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_WindowPropagation)
        elif sys.platform == "darwin":
            # macOS 系统
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_MacFrameworkScaled)
        
        self.setWindowIcon(QtGui.QIcon(get_icon_path()))
        
        self.config = load_config()
        set_language(self.config.get("language", "en"))
        
        self.corners = []
        self.corner_color = QtGui.QColor(*self.config.get("color", [0, 0, 0]))
        self.anti_burn_in_enabled = self.config.get("anti_burn_in", False)
        self.transparent_mouse_enabled = self.config.get("transparent_mouse", False)
        self.hide_on_startup = self.config.get("hide_on_startup", False)
        self.close_action = self.config.get("close_action", None)
        self.current_theme = get_system_theme()
        self.tray_icon = None  # 稍后设置

        self.build_ui()
        self.apply_theme()
        self.refresh_corners()

        # 连接全局语言信号
        language_signal.changed.connect(self.on_language_changed)
        
        app = QtWidgets.QApplication.instance()
        if app:
            app.screenAdded.connect(self.refresh_corners)
            app.screenRemoved.connect(self.refresh_corners)
            
    def on_language_changed(self):
        """处理语言改变事件"""
        # 重新加载配置
        self.config = load_config()
        # 更新语言
        set_language(self.config.get("language", "en"))
        # 刷新UI
        self.update_ui_language()
        # 应用主题（确保颜色等也更新）
        self.apply_theme()
        
    def on_theme_changed(self, theme):
        """处理主题变化事件"""
        self.current_theme = theme
        self.apply_theme()
    
    def build_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(15) # 控制控件间距
        
        # 应用标题
        self.title_label = QtWidgets.QLabel(tr("app_name"))
        title_font = QtGui.QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.title_label)
        
        # 添加标题下方间距
        spacer_label = QtWidgets.QLabel()
        spacer_label.setFixedHeight(1)  # 调整这个值改变间距大小
        spacer_label.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Fixed
        )
        main_layout.addWidget(spacer_label)

        # 圆角半径部分
        radius_layout = QtWidgets.QHBoxLayout()
        radius_layout.setContentsMargins(0, 0, 0, 0)
        radius_layout.setSpacing(10)
        
        self.radius_label = QtWidgets.QLabel(tr("radius_label"))
        self.radius_label.setFixedWidth(80)
        self.radius_label.setObjectName("setting_label")  # 设置对象名用于样式表
        radius_layout.addWidget(self.radius_label)
        
        self.radius_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.radius_slider.setRange(1, 100)
        self.radius_slider.setValue(self.config.get("radius", 20))
        self.radius_slider.valueChanged.connect(self.update_radius)
        self.radius_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 5px;
                margin: 1px 1;
                background: #e0e0e0;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #5c7cfa;
                border: 1px;
                width: 12px;
                height: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }
            QSlider::handle:horizontal:pressed {
                background: #5c7cfa;
                border: 1.2px solid #ffffff;
                width: 13px;
                height: 12px;
                margin: -4.5px 0;
                border-radius: 6.5px;
            }
            QSlider::sub-page:horizontal {
                background: #5c7cfa;
                border-radius: 3px;
            }
        """)
        
        self.radius_value = QtWidgets.QLabel(str(self.radius_slider.value()))
        self.radius_value.setFixedWidth(35)
        self.radius_value.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        radius_layout.addWidget(self.radius_slider)
        radius_layout.addWidget(self.radius_value)
        main_layout.addLayout(radius_layout)

        # 颜色选择部分
        color_layout = QtWidgets.QHBoxLayout()
        color_layout.setContentsMargins(0, 0, 0, 0)
        color_layout.setSpacing(10)
        
        self.color_label = QtWidgets.QLabel(tr("color_label"))
        self.color_label.setFixedWidth(80)
        self.color_label.setObjectName("setting_label")  # 设置对象名用于样式表
        color_layout.addWidget(self.color_label)
        
        # 颜色预览按钮（圆角正方形）
        self.color_preview = QtWidgets.QPushButton()
        self.color_preview.setFixedSize(32, 32)
        self.color_preview.setStyleSheet(
            f"background-color: {self.corner_color.name()};"
            "border: 1px solid #cccccc; border-radius: 4px;"  # 圆角正方形
        )
        self.color_preview.clicked.connect(self.pick_color)
        color_layout.addWidget(self.color_preview)
        
        # 选择颜色按钮
        self.color_btn = QtWidgets.QPushButton(tr("pick_color"))
        self.color_btn.clicked.connect(self.pick_color)
        self.color_btn.setFixedWidth(112)
        color_layout.addWidget(self.color_btn)
        
        # 候选颜色按钮（5个，圆角正方形）
        self.candidate_btns = []
        color_names = ["black", "white", "dark_gray", "light_gray", "dark_blue"]
        for name in color_names:
            color = CANDIDATE_COLORS[name]
            btn = QtWidgets.QPushButton()
            btn.setFixedSize(24, 24)
            btn.setStyleSheet(
                f"background-color: {color.name()}; "
                "border: 1px solid #cccccc; border-radius: 4px;"  # 圆角正方形
            )
            btn.setToolTip(tr(name))
            btn.clicked.connect(lambda checked, c=color: self.set_corner_color(c))
            color_layout.addWidget(btn)
            self.candidate_btns.append(btn)
        
        color_layout.addStretch()
        main_layout.addLayout(color_layout)

        # 防烧屏设置（单行布局）
        burn_layout = QtWidgets.QHBoxLayout()
        burn_layout.setContentsMargins(0, 0, 0, 0)
        burn_layout.setSpacing(10)
        
        # 左边距对齐
        spacer = QtWidgets.QLabel()
        spacer.setFixedWidth(80)
        burn_layout.addWidget(spacer)
        
        self.anti_burn_check = QtWidgets.QCheckBox(tr("anti_burn_in"))
        self.anti_burn_check.setChecked(self.anti_burn_in_enabled)
        self.anti_burn_check.setToolTip(tr("anti_burn_in_tip"))
        self.anti_burn_check.stateChanged.connect(self.toggle_anti_burn_in)
        burn_layout.addWidget(self.anti_burn_check)
        
        # 增加36px间距
        burn_layout.addSpacing(36)
        
        self.burn_interval_label = QtWidgets.QLabel(tr("anti_burn_in_interval"))
        burn_layout.addWidget(self.burn_interval_label)
        
        self.burn_interval_spin = QtWidgets.QSpinBox()
        self.burn_interval_spin.setRange(1, 120)
        self.burn_interval_spin.setValue(self.config.get("burn_in_interval", 10))
        self.burn_interval_spin.valueChanged.connect(self.update_burn_interval)
        self.burn_interval_spin.setFixedWidth(60)
        burn_layout.addWidget(self.burn_interval_spin)
        
        burn_layout.addStretch()
        main_layout.addLayout(burn_layout)

        # 鼠标设置
        mouse_layout = QtWidgets.QHBoxLayout()
        mouse_layout.setContentsMargins(0, 0, 0, 0)
        mouse_layout.setSpacing(10)
        
        # 左边距对齐
        spacer = QtWidgets.QLabel()
        spacer.setFixedWidth(80)
        mouse_layout.addWidget(spacer)
        
        self.mouse_check = QtWidgets.QCheckBox(tr("transparent_mouse"))
        self.mouse_check.setToolTip(tr("transparent_mouse_tip"))
        self.mouse_check.setChecked(self.transparent_mouse_enabled)
        self.mouse_check.stateChanged.connect(self.toggle_transparent_mouse)
        mouse_layout.addWidget(self.mouse_check)
        
        # 修改为启动时隐藏主界面选项
        self.hide_on_startup_check = QtWidgets.QCheckBox(tr("hide_on_startup"))
        self.hide_on_startup_check.setToolTip(tr("hide_on_startup_tip"))
        self.hide_on_startup_check.setChecked(self.hide_on_startup)
        self.hide_on_startup_check.stateChanged.connect(self.toggle_hide_on_startup)
        mouse_layout.addWidget(self.hide_on_startup_check)
        
        mouse_layout.addStretch()
        main_layout.addLayout(mouse_layout)

        # 底部弹簧使布局顶部对齐
        main_layout.addStretch()

    def update_radius(self, val):
        # 更新数值显示
        self.radius_value.setText(str(val))
        
        for w in self.corners:
            w.radius = val
            w.update_geometry()
        self.config["radius"] = val
        save_config(self.config)

    def set_corner_color(self, color):
        """设置圆角颜色（用于候选颜色按钮）"""
        self.corner_color = color
        # 更新预览按钮颜色
        self.color_preview.setStyleSheet(
            f"background-color: {color.name()};"
            "border: 1px solid #cccccc; border-radius: 4px;"  # 圆角正方形
        )
        
        for w in self.corners:
            w.color = color
            w.update()
        
        # 保存RGB值到配置
        self.config["color"] = [color.red(), color.green(), color.blue()]
        save_config(self.config)

    def pick_color(self):
        color = QtWidgets.QColorDialog.getColor(self.corner_color, self)
        if color.isValid():
            self.set_corner_color(color)

    def toggle_anti_burn_in(self, state):
        enabled = state == QtCore.Qt.CheckState.Checked.value
        for w in self.corners:
            w.anti_burn_in = enabled
            if enabled:
                w.create_burn_in_timer()  # 确保定时器存在
            else:
                if w.burn_in_timer and w.burn_in_timer.isActive():
                    w.burn_in_timer.stop()
                w.reset_position()
        self.config["anti_burn_in"] = enabled
        save_config(self.config)

    def toggle_transparent_mouse(self, state):
        self.transparent_mouse_enabled = state == QtCore.Qt.CheckState.Checked.value
        for w in self.corners:
            w.hide_mouse = self.transparent_mouse_enabled
            if self.transparent_mouse_enabled:
                w.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.BlankCursor))
            else:
                w.unsetCursor()
        self.config["transparent_mouse"] = self.transparent_mouse_enabled
        save_config(self.config)

    # 修改为切换启动时隐藏主界面选项
    def toggle_hide_on_startup(self, state):
        self.hide_on_startup = state == QtCore.Qt.CheckState.Checked.value
        self.config["hide_on_startup"] = self.hide_on_startup
        save_config(self.config)

    def update_burn_interval(self, val):
        for w in self.corners:
            w.update_burn_in_interval(val)
        self.config["burn_in_interval"] = val
        save_config(self.config)

    def refresh_corners(self, force_reset=False):
        """刷新所有显示器的圆角窗口"""
        # 清除旧的圆角窗口
        for w in self.corners:
            w.close()
            w.deleteLater()
        self.corners.clear()

        screens = QtWidgets.QApplication.screens()
        for screen in screens:
            for pos in ['tl', 'tr', 'bl', 'br']:
                w = CornerWindow(screen, pos, self.radius_slider.value(),
                                self.corner_color, self.anti_burn_in_enabled,
                                self.transparent_mouse_enabled,
                                self.burn_interval_spin.value())
                # 如果强制重置，则重置位置
                if force_reset:
                    w.reset_position()
                QtCore.QTimer.singleShot(100, w.show)
                self.corners.append(w)

    def closeEvent(self, event):
        if self.close_action is None:
            self.show_close_dialog()
            event.ignore()
        elif self.close_action == 0:
            QtWidgets.QApplication.quit()
        else:
            self.hide()

    def show_close_dialog(self):
        """显示关闭对话框"""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(tr("close_title"))
        dialog.setFixedSize(300, 150)
        
        # 使用垂直布局作为主布局
        main_layout = QtWidgets.QVBoxLayout(dialog)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)  # 减小全局间距
        
        # 消息标签 - 居中显示
        message = QtWidgets.QLabel(tr("close_message"))
        message.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # 文本居中
        message.setWordWrap(True)
        main_layout.addWidget(message, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)  # 控件居中
        
        # 按钮布局
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.setSpacing(10)
        
        exit_btn = QtWidgets.QPushButton(tr("close_exit"))
        exit_btn.clicked.connect(lambda: self.handle_close_choice(0, dialog))
        btn_layout.addWidget(exit_btn)
        
        minimize_btn = QtWidgets.QPushButton(tr("close_minimize"))
        minimize_btn.clicked.connect(lambda: self.handle_close_choice(1, dialog))
        minimize_btn.setDefault(True)  # 设置为默认按钮
        minimize_btn.setAutoDefault(True)  # 确保可以响应回车键
        btn_layout.addWidget(minimize_btn)
        
        main_layout.addLayout(btn_layout)
        
        # 复选框 - 居中显示
        remember_check = QtWidgets.QCheckBox(tr("remember_choice"))
        main_layout.addWidget(remember_check, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)  # 控件居中
        
        dialog.exec()
    def handle_close_choice(self, choice, dialog):
        """Process user choice from close dialog"""
        remember = dialog.findChild(QtWidgets.QCheckBox).isChecked()
        
        if remember:
            self.close_action = choice
            self.config["close_action"] = choice
            save_config(self.config)
        
        dialog.accept()
        
        if choice == 0:
            QtWidgets.QApplication.quit()
        else:
            self.hide()

    def apply_theme(self):
        if not hasattr(self, 'current_theme'):
            self.current_theme = get_system_theme()
        
        # 设置窗口背景色
        if self.current_theme == "dark":
            window_bg = "#2d2d30"
            text_color = "#ffffff"
            title_color  = "#2d2d30"
            label_color = "#e0e0e0"
            value_color = "#f0f0f0"
            spinbox_bg = "#505050"
            spinbox_border = "#707070"
            button_bg = "#606060"
            button_hover = "#707070"
            button_text = "#f0f0f0"
            selection_bg = "#5c7cfa"
            slider_groove = "#505050"
            slider_border = "#6B6B6B"
            slider_handle = "#5c7cfa"
            slider_subpage = "#5c7cfa"
            border_color = "#d0d0d0"  # 更亮的边框颜色，提高对比度
        else:
            window_bg = "#f0f0f0"
            text_color = "#000000"
            title_color = "#f0f0f0"
            label_color = "#000000"
            value_color = "#000000"
            spinbox_bg = "#f0f0f0"
            spinbox_border = "#cccccc"
            button_bg = "#f0f0f0"
            button_hover = "#e0e0e0"
            button_text = "#333333"
            selection_bg = "#d0e0ff"
            slider_groove = "#e0e0e0"
            slider_border = "#D8D8D8"
            slider_handle = "#5c7cfa"
            slider_subpage = "#5c7cfa"
            border_color = "#505050"  # 更暗的边框颜色，提高对比度
        
        # 获取基础路径（确保路径正确）
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 根据主题选择调节箭头图标
        if self.current_theme == "dark":
            # 深色主题使用浅色图标
            up_arrow_file = os.path.join(base_dir, "images", "up_arrow_light.svg")
            down_arrow_file = os.path.join(base_dir, "images", "down_arrow_light.svg")
        else:
            # 浅色主题使用深色图标
            up_arrow_file = os.path.join(base_dir, "images", "up_arrow_dark.svg")
            down_arrow_file = os.path.join(base_dir, "images", "down_arrow_dark.svg")

        # 确保路径使用正斜杠（跨平台兼容）
        up_arrow_path = up_arrow_file.replace("\\", "/")
        down_arrow_path = down_arrow_file.replace("\\", "/")
        
        # 设置窗口背景色
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {window_bg};
                color: {text_color};
            }}
                    /* 添加透明工具提示样式 */
            QToolTip {{
                background-color: {window_bg};  /* 透明背景 */
                color: {text_color};            /* 文字颜色随主题变化 */
                border: 1px solid {spinbox_border}; /* 边框颜色 */
                border-radius: 4px;            /* 圆角半径 */
                padding: 2px 2px;              /* 内边距 */
            }}
        """)
        
        # 设置标签样式
        labels = [
            self.radius_label, 
            self.color_label,
            self.burn_interval_label
        ]
        for label in labels:
            label.setStyleSheet(f"color: {label_color};")
        
        # 设置数值标签样式
        self.radius_value.setStyleSheet(f"color: {value_color}; font-weight: bold;")
        
        # 设置按钮样式
        button_style = f"""
            QPushButton {{
                background-color: {button_bg};
                color: {button_text};
                border: 1px solid {spinbox_border};
                border-radius: 4px;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: {button_hover};
            }}
        """
        self.color_btn.setStyleSheet(button_style)

        # 设置SpinBox样式 - 修复按钮大小不一致问题
        spinbox_style = f"""
            QSpinBox {{
                background-color: {spinbox_bg};
                color: {text_color};
                border: 1px solid {spinbox_border};
                border-radius: 4px;
                padding: 3px;
                padding-right: 20px; /* 为箭头按钮留出足够空间 */
                selection-background-color: {selection_bg};  /* 选中文本的背景色 */
                selection-color: {text_color};             /* 选中文本的颜色 */
            }}
            /* 按钮容器 */
            QSpinBox::up-button, QSpinBox::down-button {{
                subcontrol-origin: border;
                background-color: {spinbox_bg};
                border: 1px solid {spinbox_border};
                border-radius: 2px;
                width: 16px; /* 固定宽度 */
                height: 9px; /* 固定高度 - 确保两个按钮相同 */
                margin: 0;
            }}
            /* 上按钮位置 */
            QSpinBox::up-button {{
                subcontrol-position: top right;
                top: 2px;
                right: 2px;
                border-bottom-left-radius: 0;
                border-bottom-right-radius: 0;
            }}
            /* 下按钮位置 */
            QSpinBox::down-button {{
                subcontrol-position: bottom right;
                bottom: 2px;
                right: 2px;
                border-top-left-radius: 0;
                border-top-right-radius: 0;
            }}
            /* 按钮悬停效果 */
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
                background-color: {button_hover};
            }}
            /* 上箭头图标 */
            QSpinBox::up-arrow {{
                width: 8px;
                height: 8px;
                image: url("{up_arrow_path}");
            }}
            /* 下箭头图标 */
            QSpinBox::down-arrow {{
                width: 8px;
                height: 8px;
                image: url("{down_arrow_path}");
            }}
        """
        self.burn_interval_spin.setStyleSheet(spinbox_style)
        
        # 设置滑块样式
        slider_style = f"""
            QSlider::groove:horizontal {{
                height: 5px;
                margin: 1px 1px; 
                background: {slider_groove};
                border: 1px solid {slider_border};
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: {slider_handle};
                border: 1px solid {text_color};
                width: 12px;
                height: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }}
            QSlider::handle:horizontal:pressed {{
                background: {slider_handle};
                border: 1.2px solid {text_color};
                width: 13px;
                height: 13px;
                margin: -4.5px 0;
                border-radius: 6.5px;
            }}
            QSlider::sub-page:horizontal {{
                background: {slider_subpage};
                border-radius: 4px;
            }}
        """
        self.radius_slider.setStyleSheet(slider_style)
        
        # 设置复选框文本颜色
        checkbox_style = f"color: {label_color};"
        self.anti_burn_check.setStyleSheet(checkbox_style)
        self.mouse_check.setStyleSheet(checkbox_style)
        self.hide_on_startup_check.setStyleSheet(checkbox_style)
        
        # 设置颜色预览和候选颜色按钮的边框颜色
        preview_style = f"""
            background-color: {self.corner_color.name()};
            border: 1px solid {border_color};
            border-radius: 4px;
        """
        self.color_preview.setStyleSheet(preview_style)
        
        # 更新候选颜色按钮的边框
        for btn in self.candidate_btns:
            bg_color = btn.palette().button().color().name()
            btn.setStyleSheet(f"""
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 4px;
            """)
        
        # 设置窗口图标
        icon_path = get_icon_path()
        if icon_path:
            self.setWindowIcon(QtGui.QIcon(icon_path))
        
        # 设置标题样式
        self.setWindowTitle
        self.title_label.setStyleSheet(f"color: {text_color};" f"background-color: {title_color}")

    def update_ui_language(self):
        """更新所有UI元素的文本内容"""
        self.setWindowTitle(tr("app_name"))
        
        # 更新所有标签文本
        self.title_label.setText(tr("app_name"))
        self.title_label.setText(tr("app_name"))
        self.radius_label.setText(tr("radius_label"))
        self.color_label.setText(tr("color_label"))
        self.color_btn.setText(tr("pick_color"))
        self.anti_burn_check.setText(tr("anti_burn_in"))
        self.anti_burn_check.setToolTip(tr("anti_burn_in_tip"))
        self.burn_interval_label.setText(tr("anti_burn_in_interval"))
        self.mouse_check.setText(tr("transparent_mouse"))
        self.mouse_check.setToolTip(tr("transparent_mouse_tip"))
        self.hide_on_startup_check.setText(tr("hide_on_startup"))
        self.hide_on_startup_check.setToolTip(tr("hide_on_startup_tip"))
        
        # 更新候选颜色工具提示
        color_names = ["black", "white", "dark_gray", "light_gray", "dark_blue"]
        for i, name in enumerate(color_names):
            self.candidate_btns[i].setToolTip(tr(name))
