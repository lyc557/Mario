import pygame
from .config import *
from .sprites.mario import Mario
from .levels.level import Level
from .utils.save_system import SaveSystem

class Game:
    def __init__(self):
        self.save_system = SaveSystem()
        
        # 尝试加载存档
        save_data = self.save_system.load_game()
        if save_data:
            self.current_level = save_data['current_level']
            self.game_won = save_data['game_won']
            self.game_over = save_data['game_over']
        else:
            self.current_level = 1
            self.game_won = False
            self.game_over = False
            
        self.max_levels = 3
        self.mario = Mario()
        if save_data:
            self.mario.lives = save_data['lives']
            
        self.load_level(self.current_level)
        self.victory_timer = 0
        self.level_complete = False
        self.transition_timer = 0
        
        # 字体设置
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        self.victory_text = self.font.render('胜利！', True, FLAG_COLOR)
        self.victory_rect = self.victory_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        self.game_over_text = self.font.render('游戏结束', True, RED)
        self.game_over_rect = self.game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        self.restart_text = self.small_font.render('按R键重新开始', True, BLUE)
        self.restart_rect = self.restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
        self.save_text = self.small_font.render('按S键保存游戏', True, GREEN)
        self.save_rect = self.save_text.get_rect(topleft=(10, 70))
        
    def reset_game(self):
        self.current_level = 1
        self.mario = Mario()
        self.load_level(self.current_level)
        self.game_won = False
        self.game_over = False
        self.level_complete = False
        self.save_system.delete_save()
        
    def load_level(self, level_number):
        self.level = Level(level_number)
        self.mario.reset_position()
        self.level_complete = False
        
    def update(self):
        if not self.game_won and not self.level_complete and not self.game_over:
            if self.mario.update(self.level.platforms, self.level.enemies):
                if self.mario.lives <= 0:
                    self.game_over = True
                else:
                    self.load_level(self.current_level)
                    
            for enemy in self.level.enemies:
                enemy.update(self.level.platforms)
                
            if self.level.flag.check_collision(self.mario):
                self.level_complete = True
                self.transition_timer = pygame.time.get_ticks()
                
        if self.level_complete:
            current_time = pygame.time.get_ticks()
            if current_time - self.transition_timer >= 2000:
                if self.current_level < self.max_levels:
                    self.current_level += 1
                    self.load_level(self.current_level)
                else:
                    self.game_won = True
                    self.victory_timer = pygame.time.get_ticks()
                    
        if self.game_won:
            current_time = pygame.time.get_ticks()
            if current_time - self.victory_timer >= 2000:
                self.game_over = True
        return True
        
    def save_game(self):
        if not self.game_over and not self.level_complete:
            success = self.save_system.save_game(self)
            return success
        return False
        
    def draw(self, screen):
        screen.fill(SKY_BLUE)
        
        self.level.update_camera(self.mario.x)
        
        for platform in self.level.platforms:
            screen_x, screen_y = self.level.get_screen_position(platform.rect.x, platform.rect.y)
            platform_rect = pygame.Rect(screen_x, screen_y, platform.rect.width, platform.rect.height)
            pygame.draw.rect(screen, GREEN, platform_rect)
            
        for enemy in self.level.enemies:
            if enemy.alive:
                screen_x, screen_y = self.level.get_screen_position(enemy.x, enemy.y)
                enemy_rect = pygame.Rect(screen_x, screen_y, enemy.width, enemy.height)
                pygame.draw.rect(screen, ENEMY_COLOR, enemy_rect)
                head_rect = pygame.Rect(screen_x, screen_y, enemy.width, enemy.height//2)
                pygame.draw.rect(screen, RED, head_rect)
                
        castle_x, castle_y = self.level.get_screen_position(self.level.castle.x, self.level.castle.y)
        self.level.castle.rect.x = castle_x
        self.level.castle.rect.y = castle_y
        self.level.castle.draw(screen)
        
        flag_x, flag_y = self.level.get_screen_position(self.level.flag.x, self.level.flag.y)
        self.level.flag.rect.x = flag_x
        self.level.flag.rect.y = flag_y
        self.level.flag.draw(screen)
        
        screen_x, screen_y = self.level.get_screen_position(self.mario.x, self.mario.y)
        self.mario.rect.x = screen_x
        self.mario.rect.y = screen_y
        self.mario.draw(screen)
        
        level_text = self.small_font.render(f'关卡 {self.current_level}', True, BLUE)
        lives_text = self.small_font.render(f'生命 x {self.mario.lives}', True, RED)
        screen.blit(level_text, (10, 10))
        screen.blit(lives_text, (10, 40))
        screen.blit(self.save_text, self.save_rect)
        
        if self.level_complete and not self.game_won:
            complete_text = self.font.render(f'第{self.current_level}关完成！', True, YELLOW)
            complete_rect = complete_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            screen.blit(complete_text, complete_rect)
            
        if self.game_won:
            screen.blit(self.victory_text, self.victory_rect)
            
        if self.game_over:
            screen.blit(self.game_over_text, self.game_over_rect)
            screen.blit(self.restart_text, self.restart_rect) 