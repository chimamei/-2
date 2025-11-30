import json  
class GameStats:
    """游戏统计信息类：管理游戏中的统计数据（得分、等级、剩余飞船、最高分等）"""
    
    def __init__(self, ai_game):
        """初始化游戏统计信息"""
        self.settings = ai_game.settings  # 获取游戏设置
        self.game_active = False  # 游戏活动状态（False表示游戏未开始/结束）
        
        self._load_high_score()  # 从文件加载历史最高分
        
        self.reset_stats()  # 初始化/重置游戏的动态统计数据

    def _load_high_score(self):
        """从JSON文件加载历史最高分（私有方法，仅内部调用）"""
        filename = 'high_score.json'  # 存储最高分的文件名
        self.high_score = 0  # 默认最高分初始化为0
        
        try:
            # 尝试打开文件并读取最高分
            with open(filename) as f:
                self.high_score = json.load(f)  # 解析JSON数据
        except (FileNotFoundError, json.JSONDecodeError):
            # 文件不存在或数据格式错误时，使用默认值0
            pass 

    def reset_stats(self):
        """重置游戏的动态统计数据（新游戏开始或飞船被击中时调用）"""
        self.ships_left = self.settings.ship_limit  # 剩余飞船数量（初始为设置的飞船总数）
        self.score = 0   # 当前得分重置为0
        self.level = 1   # 当前等级重置为1
        self.settings.initialize_dynamic_settings()  # 重置游戏动态设置（速度等）
