import pygame
import random

# 屏幕常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 852)
# 刷新帧率
FRAME_PER_SEC = 60
# 创建敌人定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 敌机出现速率
ENEMY_TIME = 1000
# 英雄开火定时器常量
HERO_FIRE_EVENT = pygame.USEREVENT + 1
# 英雄开火速率
HERO_FIRE_TIME = 500

class GameSprite(pygame.sprite.Sprite):
    """ 飞机大战游戏精灵 """
    def __init__(self, image_name, speed = 1):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.speed = speed
        self.rect = self.image.get_rect()
        
    def update(self):
        # 敌军向下移动
        self.rect.y += self.speed


class Background(GameSprite):
    """ 游戏背景精灵 """
    def __init__(self, is_alt = False):
        super().__init__("../image/background.png")
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        # 1. 调用父类的垂直移动
        super().update()
        # 2. 对是否溢出屏幕
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    def __init__(self):
        # 1. 创建敌机精灵,制定敌机图片
        super().__init__("../image/enemy0.png")
        # 2. 制定敌机初始速度
        self.speed = random.randint(1, 5)
        # 3. 制定敌机初始位置
        self.rect.bottom = 0
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)

    def update(self):
        # 1. 调用父类的方法,保持垂直飞行
        super().update()
        # 2. 判断出了屏幕,删除精灵组中的飞机
        if self.rect.y >= SCREEN_RECT.height:
            self.kill()

    
class Hero(GameSprite):
    """ 英雄精灵 """
    def __init__(self):
        super().__init__("../image/hero.gif", 0)
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120

        # 创建子弹
        self.bullet_group = pygame.sprite.Group()

    def update(self):
        # 英雄水平移动
        self.rect.x += self.speed

        # 英雄边界控制
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        for i in range(3):
            bullet = Bullet()
            bullet.rect.bottom = self.rect.y - i * 40
            bullet.rect.centerx = self.rect.centerx
            self.bullet_group.add(bullet)


class Bullet(GameSprite):
    def __init__(self):
        super().__init__("../image/bullet-1.gif", -4)
    
    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()