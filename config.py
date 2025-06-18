# config.py
import os
import json

CONFIG_PATH = os.path.join(os.path.expanduser("~"), "RoundedCornersConfig.json")

DEFAULT_CONFIG = {
    "radius": 10,
    "color": [0, 0, 0],  # RGB
    "anti_burn_in": False,
    "burn_in_interval": 10,
    "transparent_mouse": True,
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
                # 添加配置验证
                for key in DEFAULT_CONFIG:
                    if key not in config:
                        config[key] = DEFAULT_CONFIG[key]
                return config
        except Exception as e:
            print(f"[Config] 加载失败: {e}")
            # 备份损坏的配置文件
            try:
                os.rename(CONFIG_PATH, f"{CONFIG_PATH}.backup")
                print(f"[Config] 已备份损坏的配置文件")
            except:
                pass
    return DEFAULT_CONFIG.copy()

def save_config(config: dict):
    """保存配置到文件"""
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"[Config] 保存失败: {e}")
        import traceback
        traceback.print_exc()

def get_config_path() -> str:
    return CONFIG_PATH
