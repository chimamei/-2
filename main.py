import sys
import pygame
import random
from time import sleep 
import json

from settings import Settings
from ship import Ship 
from bullet import Bullet 
from alien import Alien 
from game_stats import GameStats 
from button import Button 
from scoreboard import Scoreboard 

class AlienInvasion:
    """管理游戏资源和行为的主类"""
    
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        pygame.mixer.init()  # 初始化混音器（用于音效播放）
        self.settings = Settings()
        
        # 创建游戏窗口
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        
        # 创建游戏统计信息、记分板
        self.stats = GameStats(self) 
        self.sb = Scoreboard(self) 

        # 创建飞船、子弹组、外星人组
        self.ship = Ship(self) 
        self.bullets = pygame.sprite.Group() 
        self.alien_bullets = pygame.sprite.Group()  # 外星人子弹组
        self.aliens = pygame.sprite.Group() 

        # 创建外星人舰队
        self._create_fleet() 

        # 创建Play按钮
        self.play_button = Button(self, "Play") 

        # 外星人发射子弹的计时器
        self.alien_shoot_timer = 0
        self.alien_shoot_interval = 2000  # 初始发射间隔（毫秒）
        
        # 升级子弹奖励标记
        self.last_upgrade_score = 0

        # 加载游戏音效
        self._load_sounds()

    def _load_sounds(self):
        """加载游戏音效（添加错误处理）"""
        try:
            self.shoot_sound = pygame.mixer.Sound(self.settings.shoot_sound_path)
            self.explosion_sound = pygame.mixer.Sound(self.settings.explosion_sound_path)
            self.upgrade_sound = pygame.mixer.Sound(self.settings.upgrade_sound_path)
            self.ship_hit_sound = pygame.mixer.Sound(self.settings.ship_hit_sound_path)
            
            # 调整音量
            self.shoot_sound.set_volume(0.3)
            self.explosion_sound.set_volume(0.4)
            self.upgrade_sound.set_volume(0.5)
            self.ship_hit_sound.set_volume(0.4)
            
        except pygame.error as e:
            print(f"警告：音效加载失败 - {e}")
            # 创建空音效避免报错
            self.shoot_sound = pygame.mixer.Sound(pygame.mixer.Sound(buffer=1))
            self.explosion_sound = self.shoot_sound
            self.upgrade_sound = self.shoot_sound
            self.ship_hit_sound = self.shoot_sound

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()

            if self.stats.game_active: 
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_alien_bullets()
                self._alien_shoot_logic()

            self._update_screen()

    def _close_game(self):
        """保存最高分并退出游戏"""
        filename = 'high_score.json'
        high_score = self.stats.high_score
        
        try:
            with open(filename, 'w') as f:
                json.dump(high_score, f)
        except Exception as e:
            print(f"警告：无法保存最高分 - {e}")
            
        sys.exit()

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._close_game() 
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos): 
        """点击Play按钮开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats() 
            self.stats.game_active = True
            self.last_upgrade_score = 0
            
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            
            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False) 

    def _check_keydown_events(self, event):
        """响应按键按下"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q: 
            self._close_game() 
        elif event.key == pygame.K_SPACE and self.stats.game_active: 
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应按键松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """发射普通子弹并播放音效"""
        if len(self.bullets) < self.settings.bullets_allowed * 2:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.shoot_sound.play()

    def _fire_upgrade_bullets(self):
        """发射升级子弹并播放音效"""
        try:
            if not self.stats.game_active or not hasattr(self, 'ship'):
                return
            
            upgrade_bullets = [b for b in self.bullets if b.is_upgrade_bullet]
            if len(upgrade_bullets) >= 3:
                return
            
            self.upgrade_sound.play()
            for i in range(3):
                new_bullet = Bullet(self, is_upgrade_bullet=True)
                new_bullet.rect.centerx = self.ship.rect.centerx + (i - 1) * 20
                new_bullet.rect.top = self.ship.rect.top
                self.bullets.add(new_bullet)
        except Exception as e:
            print(f"升级子弹发射失败: {e}")

    def _update_bullets(self):
        """更新子弹位置并删除消失的子弹"""
        self.bullets.update()
        
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()

    def _update_alien_bullets(self):
        """更新外星人子弹位置并检测碰撞"""
        self.alien_bullets.update()
        
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(bullet)
        
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            self._ship_hit()

    def _check_bullet_alien_collisions(self):
        """响应子弹与外星人的碰撞"""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, 
            False, True
        )

        if collisions:
            self.explosion_sound.play()

        # 处理普通子弹销毁
        bullets_to_remove = []
        for bullet in self.bullets:
            if not bullet.is_upgrade_bullet and bullet in collisions:
                bullets_to_remove.append(bullet)
        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)

        # 处理得分
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

            # 检查升级奖励
            current_score = self.stats.score
            reward_score = self.settings.upgrade_bullets_reward_score
            current_reward_count = current_score // reward_score
            last_reward_count = self.last_upgrade_score // reward_score
            
            if current_reward_count > last_reward_count:
                self._fire_upgrade_bullets()
                self.last_upgrade_score = current_reward_count * reward_score

        # 清空外星人后升级关卡
        if not self.aliens: 
            self.settings.increase_speed() 
            self.stats.level += 1 
            self.sb.prep_level() 
            
            self.bullets.empty() 
            self.alien_bullets.empty()
            self._create_fleet() 

    def _alien_shoot_logic(self):
        """外星人随机发射子弹"""
        if not self.aliens:
            return
            
        current_time = pygame.time.get_ticks()
        random_interval = random.randint(1000, 3000)
        
        if current_time - self.alien_shoot_timer > random_interval:
            random_alien = random.choice(list(self.aliens))
            self.current_shooter = random_alien
            
            if len(self.alien_bullets) < self.settings.alien_bullets_allowed:
                new_bullet = Bullet(self, is_alien_bullet=True)
                self.alien_bullets.add(new_bullet)
            
            self.alien_shoot_timer = current_time

    def _create_alien(self, x_position, y_position):
        """创建单个外星人"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position 
        self.aliens.add(new_alien)

    def _create_fleet(self):
        """创建外星人舰队"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size 

        current_x = alien_width 
        current_y = alien_height 
        
        while current_y < (self.settings.screen_height - (3 * alien_height)):
            while current_x < (self.settings.screen_width - (2 * alien_width)):
                self._create_alien(current_x, current_y) 
                current_x += 2 * alien_width 
            
            current_x = alien_width 
            current_y += 2 * alien_height 

    def _check_fleet_edges(self):
        """检测外星人是否到达屏幕边缘"""
        for alien in self.aliens.sprites():
            if alien.check_edges(): 
                self._change_fleet_direction() 
                break
    
    def _change_fleet_direction(self):
        """下移舰队并改变方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed 
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """更新外星人位置"""
        self._check_fleet_edges() 
        self.aliens.update() 

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """检测外星人是否到达屏幕底部"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom: 
                self._ship_hit() 
                break

    def _ship_hit(self):
        """响应飞船被击中"""
        if self.stats.ships_left > 0:
            self.ship_hit_sound.play()
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            
            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()
            
            self._create_fleet() 
            self.ship.center_ship() 
            
            sleep(0.5)
        else:
            self.stats.game_active = False 
            pygame.mouse.set_visible(True) 
    
    def _update_screen(self):
        """更新屏幕显示"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme() 
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet() 
        for bullet in self.alien_bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen) 
        self.sb.show_score() 

        if not self.stats.game_active: 
            self.play_button.draw_button()

        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()