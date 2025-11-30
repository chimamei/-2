import pygame.font 
from pygame.sprite import Group  

from ship import Ship  

class Scoreboard:
    """记分板类：负责管理游戏中的得分显示、最高分、等级和剩余飞船数量"""
    
    def __init__(self, ai_game):
        """初始化记分板的属性"""
        self.ai_game = ai_game  # 保存游戏主实例的引用
        self.screen = ai_game.screen  # 获取游戏屏幕对象
        self.screen_rect = self.screen.get_rect()  # 获取屏幕的矩形区域（用于定位）
        self.settings = ai_game.settings  # 获取游戏设置
        self.stats = ai_game.stats  # 获取游戏统计信息（得分、等级等）

        # 设置文本颜色和字体
        self.text_color = (30, 30, 30)  # 文本颜色：深灰色
        self.font = pygame.font.SysFont(None, 48)  # 使用默认字体，字号48

        # 初始化各类得分和信息的图像渲染
        self.prep_score()  # 准备当前得分的图像
        self.prep_high_score()  # 准备最高分的图像
        self.prep_level()  # 准备当前等级的图像
        self.prep_ships()  # 准备剩余飞船数量的显示

    def prep_score(self):
        """将当前得分转换为渲染的图像（格式化显示）"""
        # 将得分四舍五入到最近的10的倍数（如1234→1230）
        rounded_score = round(self.stats.score, -1)
        # 格式化得分，添加千位分隔符（如1000→1,000）
        score_str = "{:,}".format(rounded_score) 
        # 渲染得分文本为图像（抗锯齿=True，文本颜色，背景色）
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)

        # 设置得分图像的位置：屏幕右侧，距离右边20像素，顶部20像素
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高分转换为渲染的图像（格式化显示）"""
        # 同样四舍五入并格式化最高分
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        # 渲染最高分图像
        self.high_score_image = self.font.render(high_score_str, True,
                                            self.text_color, self.settings.bg_color)

        # 设置最高分图像位置：屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top  # 与当前得分顶部对齐

    def prep_level(self):
        """将当前等级转换为渲染的图像"""
        # 将等级转换为字符串
        level_str = str(self.stats.level)
        # 渲染等级图像
        self.level_image = self.font.render(level_str, True,
                                            self.text_color, self.settings.bg_color)
        
        # 设置等级图像位置：当前得分下方，右侧对齐
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right  # 与得分右侧对齐
        self.level_rect.top = self.score_rect.bottom + 10  # 得分下方10像素

    def prep_ships(self):
        """显示剩余的飞船数量（用飞船图标表示）"""
        self.ships = Group()  # 创建精灵组存储飞船图标
        # 根据剩余飞船数量创建对应的飞船图标
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)  # 创建飞船实例
            # 设置飞船图标位置：屏幕左上角，依次排列
            ship.rect.x = 10 + ship_number * (ship.rect.width + 10)  # 间隔10像素
            ship.rect.y = 10  # 距离顶部10像素
            self.ships.add(ship)  # 添加到精灵组

    def check_high_score(self):
        """检查当前得分是否超过最高分，如果是则更新最高分"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score  # 更新最高分
            self.prep_high_score()  # 重新渲染最高分图像

    def show_score(self):
        """在屏幕上绘制所有得分信息和剩余飞船"""
        self.screen.blit(self.score_image, self.score_rect)  # 绘制当前得分
        self.screen.blit(self.high_score_image, self.high_score_rect)  # 绘制最高分
        self.screen.blit(self.level_image, self.level_rect)  # 绘制等级
        self.ships.draw(self.screen)  # 绘制剩余飞船图标
