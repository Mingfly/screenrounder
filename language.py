# language.py
from utils import get_system_language

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
        "anti_burn_in": "启用防烧屏",
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
            "当前版本: 2.1.0"
        ),
        "black": "纯黑",
        "white": "纯白",
        "dark_gray": "深灰",
        "light_gray": "浅灰",
        "dark_blue": "深蓝",
        "dark_green": "深绿",
        "dark_red": "深红",
        "pick_color": "选择颜色...",
        "Language options": "语言选项",
        "close": "关闭",
        "minimize": "最小化",
        "transparent_mouse": "隐藏圆角区域鼠标",
        "transparent_mouse_tip": "在圆角区域隐藏鼠标光标",
        "hide_on_startup": "启动时隐藏主界面",
        "hide_on_startup_tip": "程序启动时自动隐藏主设置窗口",
        "close_title": "关闭程序",
        "close_message": "您希望如何操作？",
        "close_exit": "退出程序",
        "close_minimize": "最小化到系统托盘",
        "remember_choice": "记住我的选择",
        "already_running_title": "程序已运行",
        "already_running_message": "程序已在后台运行！",
        "already_running_info": "请检查系统托盘或任务管理器。",
        "confirm_button": "确认",
        "acknowledge":"知悉"
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
        "anti_burn_in": "Enable Anti-Burn-in",
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
            "Version: 2.1.0"
        ),
        "black": "Black",
        "white": "White",
        "dark_gray": "Dark Gray",
        "light_gray": "Light Gray",
        "dark_blue": "Dark Blue",
        "dark_green": "Dark Green",
        "dark_red": "Dark Red",
        "pick_color": "Pick Color...",
        "Language options": "Language options",
        "close": "Close",
        "minimize": "Minimize",
        "transparent_mouse": "Hide mouse in corners",
        "transparent_mouse_tip": "Hide mouse cursor in rounded corner areas",
        "hide_on_startup": "Hide on Startup",
        "hide_on_startup_tip": "Hide the main window when application starts",
        "close_title": "Close Program",
        "close_message": "What would you like to do?",
        "close_exit": "Exit Program",
        "close_minimize": "Minimize to System Tray",
        "remember_choice": "Remember my choice",
        "already_running_title": "Program Already Running",
        "already_running_message": "The program is already running in background!",
        "already_running_info": "Please check system tray or task manager.",
        "confirm_button": "OK",
        "acknowledge":"OK"
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
        "anti_burn_in": "Activer anti-brûlure",
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
            "Version: 2.1.0"
        ),
        "black": "Noir",
        "white": "Blanc",
        "dark_gray": "Gris foncé",
        "light_gray": "Gris clair",
        "dark_blue": "Bleu foncé",
        "dark_green": "Vert foncé",
        "dark_red": "Rouge foncé",
        "pick_color": "Choisir la couleur...",
        "Language options": "Options de langue",
        "close": "Fermer",
        "minimize": "Réduire",
        "transparent_mouse": "Masquer souris dans les coins",
        "transparent_mouse_tip": "Masquer le curseur de la souris dans les zones de coins arrondis",
        "hide_on_startup": "Masquer au démarrage",
        "hide_on_startup_tip": "Masquer la fenêtre principale au démarrage de l'application",
        "close_title": "Fermer le programme",
        "close_message": "Que souhaitez-vous faire ?",
        "close_exit": "Quitter le programme",
        "close_minimize": "Réduire dans la barre système",
        "remember_choice": "Se souvenir de mon choix",
        "already_running_title": "Programme déjà en cours d'exécution",
        "already_running_message": "Le programme est déjà en cours d'exécution en arrière-plan !",
        "already_running_info": "Veuillez vérifier la barre d'état système ou le gestionnaire des tâches.",
        "confirm_button": "OK",
        "acknowledge":"OK"
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
        "anti_burn_in": "焼付防止を有効にする",
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
            "バージョン: 2.1.0"
        ),
        "black": "純黒",
        "white": "純白",
        "dark_gray": "濃い灰色",
        "light_gray": "薄い灰色",
        "dark_blue": "濃い青",
        "dark_green": "濃い緑",
        "dark_red": "濃い赤",
        "pick_color": "色を選択...",
        "Language options": "言語設定",
        "close": "閉じる",
        "minimize": "最小化",
        "transparent_mouse": "コーナーでマウスを非表示",
        "transparent_mouse_tip": "角丸領域でマウスカーソルを非表示にする",
        "hide_on_startup": "起動時にメイン画面を非表示",
        "hide_on_startup_tip": "アプリ起動時にメイン設定ウィンドウを自動非表示",
        "close_title": "プログラムを閉じる",
        "close_message": "どの操作を実行しますか？",
        "close_exit": "プログラムを終了",
        "close_minimize": "システムトレイに最小化",
        "remember_choice": "選択を記憶",
        "already_running_title": "プログラムは既に実行中です",
        "already_running_message": "プログラムはバックグラウンドで実行中です！",
        "already_running_info": "システムトレイまたはタスクマネージャーを確認してください。",
        "confirm_button": "確認",
        "acknowledge":"わかる"
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
        "anti_burn_in": "번인 방지 활성화",
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
            "버전: 2.1.0"
        ),
        "black": "순수 검정",
        "white": "순수 흰색",
        "dark_gray": "어두운 회색",
        "light_gray": "밝은 회색",
        "dark_blue": "어두운 파랑",
        "dark_green": "어두운 초록",
        "dark_red": "어두운 빨강",
        "pick_color": "색상 선택...",
        "Language options": "언어 옵션",
        "close": "닫기",
        "minimize": "최소화",
        "transparent_mouse": "코너에서 마우스 숨기기",
        "transparent_mouse_tip": "둥근 모서리 영역에서 마우스 커서 숨기기",
        "hide_on_startup": "시작 시 주 창 숨기기",
        "hide_on_startup_tip": "응용 프로그램 시작 시 기본 설정 창 자동 숨기기",
        "close_title": "프로그램 닫기",
        "close_message": "어떤 작업을 실행하시겠습니까?",
        "close_exit": "프로그램 종료",
        "close_minimize": "시스템 트레이로 최소화",
        "remember_choice": "선택 기억",
        "already_running_title": "프로그램이 이미 실행 중입니다",
        "already_running_message": "프로그램이 백그라운드에서 실행 중입니다!",
        "already_running_info": "시스템 트레이 또는 작업 관리자를 확인하세요.",
        "confirm_button": "확인",
        "acknowledge":"감사"
    }
}

# 当前语言
CURRENT_LANG = get_system_language(LANGUAGES.keys())

def set_language(lang_code: str):
    """设置语言代码"""
    global CURRENT_LANG
    if lang_code in LANGUAGES:
        CURRENT_LANG = lang_code

def tr(key: str) -> str:
    """翻译函数"""
    return LANGUAGES.get(CURRENT_LANG, LANGUAGES["en"]).get(key, key)

def get_language_list():
    return [(code, data["language_name"]) for code, data in LANGUAGES.items()]