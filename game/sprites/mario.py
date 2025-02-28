import pygame
import os
from ..config import *

def load_mario_images():
    mario_images = {
        'idle_right': pygame.image.load(os.path.join('assets', 'mario_idle.png')),
        'idle_left': None,
        'run_right': [],
        'run_left': [],
        'jump_right': pygame.image.load(os.path.join('assets', 'mario_jump.png')),
        'jump_left': None,
    }
    
    for i in range(3):
        img = pygame.image.load(os.path.join('assets', f'mario_run_{i}.png'))
        mario_images['run_right'].append(img)
    
    mario_images['idle_left'] = pygame.transform.flip(mario_images['idle_right'], True, False)
    mario_images['jump_left'] = pygame.transform.flip(mario_images['jump_right'], True, False)
    mario_images['run_left'] = [pygame.transform.flip(img, True, False) for img in mario_images['run_right']]
    
    return mario_images

class Mario:
    def __init__(self):
        self.width = 30
        self.height = 50
        self.x = 100
        self.y = WINDOW_HEIGHT - self.height - 50
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.vel_y = 0
        self.jumping = False
        self.direction = "right"
        self.lives = 3
        
    def move(self, direction):
        self.direction = direction
        if direction == "left":
            self.x -= MARIO_SPEED
        elif direction == "right":
            self.x += MARIO_SPEED
            
    def stop(self):
        pass
        
    def jump(self):
        if not self.jumping:
            self.vel_y = JUMP_SPEED
            self.jumping = True
            
    def reset_position(self):
        self.x = 100
        self.y = WINDOW_HEIGHT - self.height - 50
        self.vel_y = 0
        self.jumping = False
        
    def update(self, platforms, enemies):
        # 应用重力
        self.vel_y += GRAVITY
        self.y += self.vel_y
        
        # 更新碰撞盒
        self.rect.x = self.x
        self.rect.y = self.y
        
        # 检查平台碰撞
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # 从上方碰撞
                    self.rect.bottom = platform.rect.top
                    self.y = self.rect.y
                    self.vel_y = 0
                    self.jumping = False
                elif self.vel_y < 0:  # 从下方碰撞
                    self.rect.top = platform.rect.bottom
                    self.y = self.rect.y
                    self.vel_y = 0
                    
        # 检查敌人碰撞
        for enemy in enemies:
            if enemy.alive and self.rect.colliderect(enemy.rect):
                if self.vel_y > 0 and self.rect.bottom <= enemy.rect.centery:
                    enemy.alive = False
                    self.vel_y = JUMP_SPEED
                else:
                    self.lives -= 1
                    return True
                    
        # 检查边界
        if self.x < 0:
            self.x = 0
        elif self.x > LEVEL_WIDTH - self.width:
            self.x = LEVEL_WIDTH - self.width
            
        if self.y > WINDOW_HEIGHT:
            self.lives -= 1
            return True
            
        return False
        
    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect) 