import pygame
from ..config import * # 从父级目录（..）的 config 模块导入所有内容（*）

class Flag:
    """
    Flag 类表示游戏中的旗帜对象。
    """
    def __init__(self, x, y):
        """
        初始化 Flag 对象。

        Args:
            x (int): 旗杆左上角的 x 坐标。
            y (int): 旗杆左上角的 y 坐标。
        """
        self.width = 10  # 旗杆的宽度
        self.height = 200 # 旗杆的高度
        self.x = x      # 旗杆的 x 坐标
        self.y = y      # 旗杆的 y 坐标
        self.rect = pygame.Rect(x, y, self.width, self.height) # 创建旗杆的矩形区域，用于碰撞检测
        self.flag_width = 40  # 旗帜的宽度
        self.flag_height = 30 # 旗帜的高度

    def check_collision(self, mario):
        """
        检查旗帜与马里奥是否发生碰撞。

        Args:
            mario (pygame.Rect): 马里奥的矩形区域。

        Returns:
            bool: 如果发生碰撞，则返回 True；否则返回 False。
        """
        return self.rect.colliderect(mario.rect)  # 使用 pygame 的 colliderect 方法进行矩形碰撞检测

    def draw(self, screen):
        """
        在屏幕上绘制旗帜。

        Args:
            screen (pygame.Surface): 要绘制的屏幕表面。
        """
        # 绘制旗杆
        pygame.draw.rect(screen, WHITE, self.rect) # 使用白色绘制旗杆矩形
        # 绘制旗帜
        flag_rect = pygame.Rect(self.x + self.width, # 旗帜的 x 坐标，位于旗杆右侧
                               self.y,             # 旗帜的 y 坐标，与旗杆顶部对齐
                               self.flag_width,
                               self.flag_height)
        pygame.draw.rect(screen, FLAG_COLOR, flag_rect) # 使用 FLAG_COLOR 绘制旗帜矩形