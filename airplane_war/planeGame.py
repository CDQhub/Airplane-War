import pygame
from plane_sprite import *

class PlaneGame(object):
    """ 飞机大战主游戏 """
    def __init__(self):
        print("游戏初始化")

        # 1. 创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2. 创建游戏时钟
        self.clock = pygame.time.Clock()
        # 3. 创建精灵和精灵组
        self.__create_sprites()
        # 4. 设置定时器事件
        # 创建敌机
        pygame.time.set_timer(CREATE_ENEMY_EVENT, ENEMY_TIME)
        # 创建英雄开火
        pygame.time.set_timer(HERO_FIRE_EVENT, HERO_FIRE_TIME)
        
    def __create_sprites(self):
        # 创建背景精灵和精灵组
        bg1 = Background()
        bg2 = Background(True)
        self.bg_group = pygame.sprite.Group((bg1, bg2))

        # 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()

        # 创建英雄的精灵和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start(self):
        print("游戏开始")

        while True:
            # 1. 设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 2. 事件监听
            self.__event_handler()
            # 3. 碰撞检测
            self.__check_collide()
            # 4. 更新/绘制精灵组
            self.__update_sprites()
            # 5. 更新显示
            pygame.display.update()
    
    def __event_handler(self):
        for event in pygame.event.get():
            # 退出游戏
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                # 创建敌机精灵
                enemy = Enemy()
                # 加入精灵组
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()
            """
            # 不能连续右移,只能松开右键才会再次触发
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                print("英雄右移")
            """
        
        # 获得按键元组
        key_pressed = pygame.key.get_pressed()
        # 判断是不是操作健
        if key_pressed[pygame.K_RIGHT]:
            self.hero.speed = 3
        elif key_pressed[pygame.K_LEFT]:
            self.hero.speed = -3
        else:
            self.hero.speed = 0

    def __check_collide(self):
        # 子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullet_group, self.enemy_group, True, True)

        # 敌机撞毁英雄
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(enemies) > 0:
            self.hero.kill()
            PlaneGame.__game_over()

    def __update_sprites(self):
        # 背景更新
        self.bg_group.update()
        self.bg_group.draw(self.screen)
        
        # 敌人更新
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        # 英雄更新
        self.hero_group.update()
        self.hero_group.draw(self.screen)

        # 子弹更新
        self.hero.bullet_group.update()
        self.hero.bullet_group.draw(self.screen)

    @staticmethod
    def __game_over():
        print("游戏结束")
        pygame.quit()
        exit()

if __name__ == '__main__':
    # 创建游戏对象
    game = PlaneGame()
    # 启动游戏
    game.start()