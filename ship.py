import pygame
from pygame.sprite import Sprite  

class Ship(Sprite):
    """飞船类：管理飞船的创建、移动和绘制"""
    
    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置"""
        super().__init__()  
        self.screen = ai_game.screen  # 获取游戏屏幕对象
        self.settings = ai_game.settings  # 获取游戏设置（包含飞船速度等参数）
        self.screen_rect = ai_game.screen.get_rect()  # 获取屏幕的矩形区域，用于定位飞船

        # 加载飞船图像并获取其矩形对象
        self.image = pygame.image.load('images/ship.png')  # 加载飞船图片
        self.rect = self.image.get_rect()  # 将图像转换为矩形对象（便于定位和碰撞检测）

        # 将飞船初始位置设置在屏幕底部中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 存储飞船的精确水平位置（使用浮点数实现平滑移动）
        self.x = float(self.rect.x)

        # 移动标志：控制飞船的左右移动状态（初始为静止）
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志更新飞船的位置（确保飞船不会移出屏幕）"""
        # 向右移动：如果右移标志为True且飞船右侧未超出屏幕
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed  # 增加x坐标（右移）
        # 向左移动：如果左移标志为True且飞船左侧未超出屏幕
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed  # 减少x坐标（左移）
        
        # 将精确的浮点数坐标同步到rect对象（rect只存储整数）
        self.rect.x = self.x
        
    def center_ship(self):
        """将飞船重置到屏幕底部中央位置（用于飞船被击中后复位）"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)  # 重置精确坐标

    def blitme(self):
        """在屏幕的指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)  # 将飞船图像绘制到rect对应的位置

