import pygame
from pygame.sprite import Sprite  

class Alien(Sprite):
    """外星人类：管理单个外星人的创建、位置更新和边缘检测"""
    
    def __init__(self, ai_game):
        """初始化外星人并设置其初始位置"""
        super().__init__()  # 调用父类Sprite的初始化方法
        self.screen = ai_game.screen  # 获取游戏屏幕对象
        self.settings = ai_game.settings  

       
        self.image = pygame.image.load('images/alien.png')  # 加载外星人图片
        self.rect = self.image.get_rect() 

        # 设置外星人的初始位置：屏幕左上角附近，留出一个外星人宽度和高度的空隙
        self.rect.x = self.rect.width  # 初始x坐标为外星人宽度（左侧留出空隙）
        self.rect.y = self.rect.height  # 初始y坐标为外星人高度（顶部留出空隙）

        # 存储外星人的精确位置（使用浮点数实现平滑移动）
        self.x = float(self.rect.x)  # 精确x坐标
        self.y = float(self.rect.y) 

    def check_edges(self):
        """检测外星人是否到达屏幕边缘（左右两侧），到达则返回True"""
        screen_rect = self.screen.get_rect()  # 获取屏幕矩形区域
        
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        return False  # 未到达边缘返回False

    def update(self):
        """更新外星人的位置（根据舰队方向移动，实现左右移动）"""
        # 外星人速度 × 舰队方向（1向右，-1向左）= 实际移动距离
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x  # 将精确坐标同步到rect对象（用于绘制）
