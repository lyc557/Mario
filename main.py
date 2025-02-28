import pygame
import sys
from game import Game, WINDOW_WIDTH, WINDOW_HEIGHT, FPS

# 初始化Pygame
pygame.init()

# 设置游戏窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("超级陆昊霖")

# 创建游戏实例
game = Game()

# 游戏主循环
clock = pygame.time.Clock()
running = True

while running:
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if not game.game_over and not game.level_complete:
                game.save_game()  # 退出时自动保存
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game.game_won and not game.level_complete:
                game.mario.jump()
            elif event.key == pygame.K_r and game.game_over:
                game.reset_game()
            elif event.key == pygame.K_s:
                if game.save_game():
                    save_success = game.small_font.render('游戏已保存！', True, (0, 255, 0))
                    save_success_rect = save_success.get_rect(center=(WINDOW_WIDTH//2, 100))
                    screen.blit(save_success, save_success_rect)
                    pygame.display.flip()
                    pygame.time.wait(1000)
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                game.mario.stop()
                
    # 获取按键状态
    keys = pygame.key.get_pressed()
    if not game.game_won and not game.level_complete and not game.game_over:
        if keys[pygame.K_LEFT]:
            game.mario.move("left")
        if keys[pygame.K_RIGHT]:
            game.mario.move("right")
    
    # 更新游戏状态
    game.update()
    
    # 绘制
    game.draw(screen)
    
    # 更新显示
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit() 