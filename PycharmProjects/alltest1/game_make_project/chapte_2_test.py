# 主游戏类
import pygame
import plane_sprite.plane_sprite as plane_sprite


class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        print("游戏初始化")
        # 1.创建游戏窗口--矩形对象的size属性就是元组
        self.screen = pygame.display.set_mode((plane_sprite.SCREEN_RECT.size))
        # 2.创建游戏时钟
        self.clock = pygame.time.Clock()
        # 3.调用私有方法，精灵和精灵组的创建
        self.__create_sprites()

    def __create_sprites(self):
        # 创建背景
        bg1 = plane_sprite.BackGroud()
        bg2 = plane_sprite.BackGroud(True)
        self.back_group = pygame.sprite.Group(bg1, bg2)

    def start_game(self):
        print("游戏开始")
        while True:
            # 1.设置刷频率
            self.clock.tick(plane_sprite.FRAME_PER_SEC)
            # 2.事件监听
            self.__event_handles()
            # 3.碰撞检测
            self.__check_collide()
            # 4，更新/绘制精灵组
            self.__update_sprites()
            # 5.更新显示
            pygame.display.update()

    def __event_handles(self):
        for even in pygame.event.get():
            # 判断是否退出游戏
            if even.type == pygame.QUIT:
                PlaneGame.__game_over()

    def __check_collide(self):
        pass

    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)

    @staticmethod
    def __game_over(cls):
        print("游戏结束")
        pygame.quit()
        exit()


if __name__ == '__main__':
    # 创建游戏对象
    game = PlaneGame()
    # 启动游戏
    game.start_game()
