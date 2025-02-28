import pygame
from ..config import *
from ..sprites.platform import Platform
from ..sprites.enemy import Enemy
from ..sprites.castle import Castle
from ..sprites.flag import Flag

class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.platforms = []
        self.enemies = []
        self.camera_x = 0
        
        # 创建地面
        ground_height = 50
        for x in range(0, LEVEL_WIDTH, 50):
            self.platforms.append(Platform(x, WINDOW_HEIGHT - ground_height, 50, ground_height))
            
        # 根据关卡号创建不同的平台和敌人
        if level_number == 1:
            # 第一关
            self.platforms.extend([
                Platform(300, 400, 200, 20),
                Platform(600, 300, 200, 20),
                Platform(900, 400, 200, 20)
            ])
            self.enemies.extend([
                Enemy(400, 300),
                Enemy(700, 200)
            ])
        elif level_number == 2:
            # 第二关
            self.platforms.extend([
                Platform(300, 300, 200, 20),
                Platform(600, 400, 200, 20),
                Platform(900, 300, 200, 20),
                Platform(1200, 400, 200, 20)
            ])
            self.enemies.extend([
                Enemy(400, 200),
                Enemy(700, 300),
                Enemy(1000, 200)
            ])
        elif level_number == 3:
            # 第三关
            self.platforms.extend([
                Platform(300, 400, 100, 20),
                Platform(500, 300, 100, 20),
                Platform(700, 200, 100, 20),
                Platform(900, 300, 100, 20),
                Platform(1100, 400, 100, 20)
            ])
            self.enemies.extend([
                Enemy(400, 300),
                Enemy(600, 200),
                Enemy(800, 100),
                Enemy(1000, 200)
            ])
            
        # 创建城堡和旗帜
        self.castle = Castle(LEVEL_WIDTH - 200, WINDOW_HEIGHT - ground_height - 150)
        self.flag = Flag(LEVEL_WIDTH - 300, WINDOW_HEIGHT - ground_height - 200)
        
    def update_camera(self, player_x):
        # 相机跟随玩家，保持玩家在屏幕中间
        self.camera_x = player_x - WINDOW_WIDTH // 2
        
        # 限制相机不超出关卡边界
        if self.camera_x < 0:
            self.camera_x = 0
        elif self.camera_x > LEVEL_WIDTH - WINDOW_WIDTH:
            self.camera_x = LEVEL_WIDTH - WINDOW_WIDTH
            
    def get_screen_position(self, x, y):
        # 将世界坐标转换为屏幕坐标
        return x - self.camera_x, y 