#clear-close_action.py
import os
import json

# 配置文件路径（与 config.py 中一致）
CONFIG_PATH = os.path.join(os.path.expanduser("~"), "RoundedCornersConfig.json")

def reset_close_action():
    """重置 close_action 配置为 None"""
    try:
        # 检查配置文件是否存在
        if not os.path.exists(CONFIG_PATH):
            print(f"配置文件不存在: {CONFIG_PATH}")
            return
        
        # 读取配置文件
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        # 重置 close_action
        if "close_action" in config:
            print(f"当前 close_action 值: {config['close_action']}")
            config["close_action"] = None
            print("已将 close_action 重置为 None")
        else:
            print("配置中未找到 close_action 字段，无需重置")
        
        # 保存修改后的配置
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        
        print("配置已成功更新")
    
    except Exception as e:
        print(f"操作失败: {e}")
        # 添加更具体的错误信息
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("正在重置关闭行为设置...")
    reset_close_action()
    print("操作完成。下次启动应用时将再次显示关闭选项对话框。")
