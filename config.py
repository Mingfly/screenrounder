import os
import json

CONFIG_PATH = os.path.join(os.path.expanduser("~"), "RoundedCornersConfig.json")

DEFAULT_CONFIG = {
    "radius": 20,
    "color": [0, 0, 0],  # RGB
    "anti_burn_in": False,
    "burn_in_interval": 10,
    "transparent_mouse": False,
    "language": "en",
    "hide_on_startup": False,
    "close_action": None  # None, 0=exit, 1=minimize
}

def load_config() -> dict:
    """从文件读取配置，失败则返回默认配置"""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
                return {**DEFAULT_CONFIG, **config}  # 覆盖默认值
        except Exception as e:
            print(f"[Config] 加载失败: {e}")
    return DEFAULT_CONFIG.copy()

def save_config(config: dict):
    """保存配置到文件"""
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"[Config] 保存失败: {e}")

def get_config_path() -> str:
    return CONFIG_PATH
