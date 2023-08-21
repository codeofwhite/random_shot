import pygame as pg

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WIDTH = 600
HEIGHT = 500
FPS = 216

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))

# chapter_1
# 按钮们
btn1_img = pg.image.load(
    'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/button_type_1.png')
btn1_img = pg.transform.scale(btn1_img, (265, 60))

# 载入图片
background_img = pg.image.load(
    'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make/img/background.png').convert()
init_bg_img = pg.image.load(
    'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/content_img.jpg')
store_img = pg.image.load(
    'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/OIG.wnRZ6M1r58iBqxJV7.1b.jpg')
store_img = pg.transform.scale(store_img, (800, 800))
help_bg = pg.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/help_bg.jpg"
)

player_img = pg.image.load(
    'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make/img/player.png').convert()
player_img.set_colorkey(BLACK)
player_img = pg.transform.scale(player_img, (50, 38))
# 缩小飞机
player_img_min = pg.transform.scale(player_img, (25, 19))
chapter2_player_img = pg.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/chapter2_player_img_99x99.png")
chapter2_player_img.set_colorkey(BLACK)
chapter2_player_img = pg.transform.scale(chapter2_player_img, (70, 58))

player_inv = pg.image.load(
    'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/player_inv.png').convert()
player_inv.set_colorkey(BLACK)
player_inv = pg.transform.scale(player_inv, (50, 38))

player_time = pg.image.load(
    'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/player_time.png').convert()
player_time.set_colorkey(BLACK)
player_time = pg.transform.scale(player_time, (50, 38))

# 双枪
player_gunup = pg.image.load(
    'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/player_gunup.png').convert()
player_gunup.set_colorkey(BLACK)
player_gunup = pg.transform.scale(player_gunup, (50, 38))

# 陨石
rock_img = pg.image.load('C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make/img/rock.png').convert()
rock_img.set_colorkey(BLACK)

# 普通子弹
bullet_img = pg.image.load(
    'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make/img/bullet.png').convert()
bullet_img.set_colorkey(BLACK)

# 镭射
laser_img = pg.image.load(
    'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/OIG.Xq_pdFx8_rCRKTlbXZzh-removebg-preview.png').convert()
laser_img = pg.transform.scale(laser_img, (100, 580))
laser_img.set_colorkey(BLACK)

rock_imgs = []
for i in range(7):
    rock_imgs.append(
        pg.image.load(f'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make/img/rock{i}.png'))

font_name = pg.font.match_font('华文行楷')

# 爆炸动画图片
expl_anim = {}
expl_anim['big'] = []
expl_anim['small'] = []
for i in range(9):
    expl_img = pg.image.load(
        f'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make/img/expl{i}.png').convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['big'].append(pg.transform.scale(expl_img, (75, 75)))
    expl_anim['small'].append(pg.transform.scale(expl_img, (50, 50)))

# 飞船死亡爆炸动画
player_expl_img = []
for i in range(9):
    expl_img = pg.image.load(
        f'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make/img/player_expl{i}.png').convert()
    expl_img.set_colorkey(BLACK)
    player_expl_img.append(expl_img)

# 生命数
player_lives_img = pg.image.load(f'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make/img/player.png')
player_lives_img = pg.transform.scale(player_lives_img, (20, 20))
player_lives_img.set_colorkey(BLACK)

# 石头掉落道具
power_imgs = {}
power_imgs['shield'] = pg.image.load(
    f'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make/img/shield.png')
power_imgs['gun'] = pg.image.load(f'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make/img/gun.png')
power_imgs['time'] = pg.transform.scale(pg.image.load(
    f'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/inv_time.png'),
    (40, 40))
power_imgs['time2'] = pg.transform.scale(pg.image.load(
    'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/time2.png'),
    (40, 40))
