import pygame
from ..config import *

class Flag:
    def __init__(self, x, y):
        self.width = 10
        self.height = 200
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.flag_width = 40
        self.flag_height = 30
        
    def check_collision(self, mario):
        return self.rect.colliderect(mario.rect)
        
    def draw(self, screen):
        # 绘制旗杆
        pygame.draw.rect(screen, WHITE, self.rect)
        # 绘制旗帜
        flag_rect = pygame.Rect(self.x + self.width, 
                              self.y, 
                              self.flag_width, 
                              self.flag_height)
        pygame.draw.rect(screen, FLAG_COLOR, flag_rect) 