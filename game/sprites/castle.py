import pygame
from ..config import *

class Castle:
    def __init__(self, x, y):
        self.width = 100
        self.height = 150
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
    def draw(self, screen):
        pygame.draw.rect(screen, CASTLE_COLOR, self.rect)

        # 塔楼
        tower_width = self.width // 3
        tower_spacing = (self.width - 3*tower_width) // 2
        
        for i in range(3):
            tower_x = self.x + i * (tower_width + tower_spacing)
            tower = pygame.Rect(tower_x, self.y, tower_width, self.height//2)
            pygame.draw.rect(screen, CASTLE_COLOR, tower)
            
            # 塔尖
            points = [
                (tower_x, self.y),
                (tower_x + tower_width//2, self.y - 20),
                (tower_x + tower_width, self.y)
            ]
            pygame.draw.polygon(screen, RED, points)
            
        # 门
        door_width = self.width // 3
        door_height = self.height // 3
        door = pygame.Rect(self.x + (self.width - door_width)//2,
                         self.y + self.height - door_height,
                         door_width, door_height)
        pygame.draw.rect(screen, BROWN, door) 