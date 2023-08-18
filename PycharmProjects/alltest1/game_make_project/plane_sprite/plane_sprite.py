# 精灵和精灵派生类；
import pygame

# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 800, 600)


class GameSprite(pygame.sprite.Sprite):

    def __init__(self, image_name, speed=1):
        # 调用父类的初始化方法
        super().__init__()
        # 定义对象的属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        # 在屏幕的垂直方向移动
        self.rect.y += self.speed


class BackGroud(GameSprite):
    """游戏背景"""

    def __init__(self, is_alt=False):
        # is_alt区分时第一张图像还是第二张
        # 1.调用父类党法完成基本设置
        super().__init__("C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make/img/background.png")
        # 2.判断是否时交替图像，如果是，需要设置初始位置
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        # 1.调用父类的方向实现，实现移动
        super().update()
        # 2.判断是否移出屏幕，如果一处屏幕，将图像设置到屏幕的上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height
