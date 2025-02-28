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
            
        self.x += self.vel_x
        self.rect.x = self.x
        
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
        
        if not self.on_ground:
            self.vel_y += GRAVITY
        
        self.y += self.vel_y
        self.rect.y = self.y
        
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.y = self.rect.y
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.y = self.rect.y
                    self.vel_y = 0
        
        if self.y > WINDOW_HEIGHT:
            self.alive = False
            
    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, ENEMY_COLOR, self.rect)
            head_height = self.height // 2
            head_rect = pygame.Rect(self.x, self.y, self.width, head_height)
            pygame.draw.rect(screen, RED, head_rect) 