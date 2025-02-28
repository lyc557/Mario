import pygame
from ..config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 40
        self.height = 40
        self.x = x
        self.y = y
        self.vel_x = ENEMY_SPEED
        self.vel_y = 0
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.alive = True
        self.on_ground = False
        
    def update(self, platforms):
        if not self.alive:
            return
            
        # 水平移动
        self.x += self.vel_x
        self.rect.x = self.x
        
        # 检查平台碰撞（水平方向）
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0:
                    self.rect.right = platform.rect.left
                    self.x = self.rect.x
                    self.vel_x *= -1
                elif self.vel_x < 0:
                    self.rect.left = platform.rect.right
                    self.x = self.rect.x
                    self.vel_x *= -1
        
        # 应用重力
        if not self.on_ground:
            self.vel_y += GRAVITY
        
        # 垂直移动
        self.y += self.vel_y
        self.rect.y = self.y
        
        # 检查平台碰撞（垂直方向）
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # 从上方碰撞
                    self.rect.bottom = platform.rect.top
                    self.y = self.rect.y
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # 从下方碰撞
                    self.rect.top = platform.rect.bottom
                    self.y = self.rect.y
                    self.vel_y = 0
        
        # 检查是否掉出屏幕
        if self.y > WINDOW_HEIGHT:
            self.alive = False
            
    def draw(self, screen):
        if self.alive:
            # 绘制敌人身体
            pygame.draw.rect(screen, ENEMY_COLOR, self.rect)
            # 绘制敌人头部
            head_height = self.height // 2
            head_rect = pygame.Rect(self.x, self.y, self.width, head_height)
            pygame.draw.rect(screen, RED, head_rect) 