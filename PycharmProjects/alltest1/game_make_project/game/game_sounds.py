import pygame as pg

pg.init()
pg.mixer.init()

# 音乐
shoot_sound = pg.mixer.Sound('C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make/sound/shoot.wav')
laser_sound = pg.mixer.Sound(
    'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/sounds/SnapInsta.io - 激光枪音效【laser gun sound】 (128 kbps).mp3')
expl_sounds = []
for i in range(2):
    expl_sounds.append(pg.mixer.Sound(f'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make/sound/expl{i}.wav'))
# 背景音乐
BGM = pg.mixer.music.load('C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make/sound/background.ogg')  # 这个会重复播放，且唯一？
pg.mixer.music.set_volume(0.3)
# 死亡音效和音乐
die_sound = pg.mixer.Sound('C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make/sound/rumble.ogg')
die_music = pg.mixer.Sound(
    'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/sounds/SnapInsta.io - 游戏结束蜂鸣声（Game over beep）_ 音樂音效 （Music Sound Effects） (128 kbps).mp3')
# 吃到奖励
gun_sound = pg.mixer.Sound('C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make/sound/pow0.wav')
shield_sound = pg.mixer.Sound('C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make/sound/pow1.wav')
time_sound = pg.mixer.Sound('C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/sounds/time_sound.mp3')
time_2_sound = pg.mixer.Sound('C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/sounds/time2.mp3')
