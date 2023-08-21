# 和pyqt会有窗口大小的冲突
import sys
import pymysql
import tkinter as tk
import cv2
import mediapipe as mp
import pygame as pg
import random
import CG

from cv2 import VideoCapture

import config
import gesture.gesture_funcs as ggf
import game.game_sounds as game_sound
import game.game_imgs as game_img
import tk_ui as tk_login
import plane_sprite.plane_sprite as plane_sprite
from pygame.locals import *
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

# 初始化pygame游戏
pg.init()
pg.mixer.init()
SIZE = WINDOWWIDTH, WINDOWHEIGHT = config.WIDTH, config.HEIGHT
screen = pg.display.set_mode(size=SIZE)
pg.display.set_caption("打飞机")
# 设置图标，封装成exe也有用
pg.display.set_icon(pg.image.load('C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make/img/player.png'))
clock = pg.time.Clock()

# 手势识别初始化
mp_drawing = mp.solutions.drawing_utils  # mediapipe 繪圖方法
mp_drawing_styles = mp.solutions.drawing_styles  # mediapipe 繪圖樣式
mp_hands = mp.solutions.hands  # mediapipe 偵測手掌方法

#  无敌时间（都可以用）间隔参数
INVINCIBLE_TIME = pg.USEREVENT + 2


def bgm1():
    # 背景音乐
    pg.mixer.music.load(
        'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make/sound/background.ogg')  # 这个会重复播放
    pg.mixer.music.set_volume(0.3)
    pg.mixer.music.play(-1)


# 玩家
class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = game_img.player_img
        self.rect = self.image.get_rect()  # 外面的框
        self.radius = 20
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = config.WIDTH / 2
        self.rect.bottom = config.HEIGHT - 10
        self.speed = 5
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0
        self.last_shot_time = 0
        self.invincible = False

    def update(self):
        now = pg.time.get_ticks()
        # print(now - self.gun_time)
        if self.gun >= 2 and now - self.gun_time > 5000:
            self.gun = 1
            self.image = game_img.player_img
        if self.hidden and pg.time.get_ticks() - self.hide_time > 3000:
            self.hidden = False
            self.image = game_img.player_img
            self.invincible = False
        if self.rect.right > config.WIDTH:
            self.rect.right = config.WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > config.HEIGHT:
            self.rect.bottom = config.HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot_right(self):
        if not self.hidden:
            current_time = pg.time.get_ticks()
            # 设置射击间隔
            if current_time - self.last_shot_time >= 300:
                if self.gun == 1:
                    bullet = Bullet(self.rect.centerx, self.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    pg.mixer.Sound.play(game_sound.shoot_sound)
                    self.last_shot_time = current_time
                elif self.gun >= 2:
                    bullet1 = Bullet(self.rect.left, self.rect.top)
                    bullet2 = Bullet(self.rect.right, self.rect.top)
                    all_sprites.add(bullet1, bullet2)
                    bullets.add(bullet1, bullet2)
                    pg.mixer.Sound.play(game_sound.shoot_sound)
                    self.last_shot_time = current_time

    def shoot_left(self):
        if not self.hidden:
            current_time = pg.time.get_ticks()
            # 设置射击间隔
            if current_time - self.last_shot_time >= 1500:
                laser = Laser(self.rect.centerx, self.rect.top)
                all_sprites.add(laser)
                lasers.add(laser)
                self.last_shot_time = current_time
                pg.mixer.Sound.play(game_sound.laser_sound)

    # 复活后的隐藏状态
    def hide(self):
        self.hidden = True
        self.hide_time = pg.time.get_ticks()
        self.image = game_img.player_inv
        self.invincible = True

    # 捡到闪电
    def gunup(self):
        if not self.hidden:
            self.gun += 1
            self.gun_time = pg.time.get_ticks()
            self.image = game_img.player_gunup

    # 捡到时钟
    def invincible_time(self):
        if not self.hidden:
            self.invincible = True
            self.image = game_img.player_time
            pg.time.set_timer(INVINCIBLE_TIME, 5000)  # 设置定时器，3秒后触发无敌时间事件


# 陨石
class Rock(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(game_img.rock_imgs)
        self.image = pg.Surface((50, 50))
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()  # 外面的框
        # pg.draw.rect(self.image, RED, self.rect)
        self.radius = self.rect.width * 0.85 / 2
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, config.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -110)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-2, 6)

    # 石头旋转
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pg.transform.rotate(self.image_ori, self.total_degree)
        # 这里的转动会造成画面的失真，需要特殊处理；括号里面用self.image会出事。也就是失真会叠加，而用一张图片当副本就可以避免
        # 解决转动时候的方块定位问题；重新定位，否则转动时就会像碰壁一样的发生弹性碰撞
        center = self.rect.center  # 中心点
        self.rect = self.image.get_rect()  # 重新定位
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > config.HEIGHT or self.rect.left > config.WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, config.WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 3)
            self.speedx = random.randrange(-3, 3)


# 一般子弹
class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = game_img.bullet_img
        self.rect = self.image.get_rect()  # 外面的框
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


# 激光柱
class Laser(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = game_img.laser_img
        # 创建一个矩形对象，表示激光的形状和位置
        self.rect = self.image.get_rect()
        # 设置激光的速度
        self.rect.centerx = x
        self.rect.bottom = y
        self.last_update = pg.time.get_ticks()
        self.speedy = -10

    # 更新方法，让激光向上移动，并检测是否超出屏幕边界
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


# 陨石爆炸效果
class Exploration(pg.sprite.Sprite):
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = game_img.expl_anim[self.size][0]
        self.rect = self.image.get_rect()  # 外面的框
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()  # 初始化到现在经过的毫秒数
        self.frame_rate = 50  # 如果不设定的话，动画会播放得太快

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(game_img.expl_anim[self.size]):  # 如果是最后一张图片的话
                self.kill()
            else:
                self.image = game_img.expl_anim[self.size][self.frame]
                # 重新定位;如果不这样做，可能会导致精灵在动画过程中移动或是抖动，就如陨石旋转那部分一样
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center


# 死亡爆炸效果
class Death(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.image = game_img.player_expl_img[0]
        self.rect = self.image.get_rect()  # 外面的框
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()  # 初始化到现在进过的毫秒数
        self.frame_rate = 50  # 如果不设定的话，动画会播放得太快

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(game_img.player_expl_img):  # 如果是最后一张图片的话
                self.kill()
            else:
                self.image = game_img.player_expl_img[self.frame]
                # 重新定位;如果不这样做，可能会导致精灵在动画过程中移动或是抖动，就如陨石旋转那部分一样
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center


# 道具
class Power(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun', 'time', 'time2'])
        self.image = game_img.power_imgs[self.type]
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()  # 外面的框
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y >= config.HEIGHT:
            self.kill()


# 初始化对象
player = Player()
bullets = pg.sprite.Group()
rocks = pg.sprite.Group()
powers = pg.sprite.Group()
lasers = pg.sprite.Group()
all_sprites = pg.sprite.Group()
all_sprites.add(player)
for i in range(20):
    rock = Rock()
    rocks.add(rock)
    all_sprites.add(rock)
score = 0


# 游戏界面显示文字
def draw_text(surf, text, size, x, y):
    font = pg.font.Font(game_img.font_name, size)
    text_surface = font.render(text, True, config.WHITE, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)


# 显示生命值
def draw_health(surf, hp, x, y, text, size, color):
    high = 20
    if hp <= 0:
        hp = 0
    if hp >= 500:
        hp = hp / 2
        high = 30
    BAR_LENGTH = hp
    BAR_HEIGHT = high
    fill = hp
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, color, fill_rect)  # 血条
    pg.draw.rect(surf, config.WHITE, outline_rect, 2)  # 血条外框
    font = pg.font.Font(game_img.font_name, size)
    text_surface = font.render(text, True, config.WHITE)
    text_rect = text_surface.get_rect()
    text_rect.x = BAR_LENGTH / 2
    text_rect.y = y
    surf.blit(text_surface, text_rect)


# 显示生命数
def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i  # 间隔像素
        img_rect.y = y
        surf.blit(img, img_rect)


# 增加陨石
def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)


font = pg.font.Font("C:/Windows/Fonts/s8514fix.fon", 32)  # 加载字体
font_zh = pg.font.Font('C:/Windows/Fonts/msyhbd.ttc', 20)

playCG = False


# 游戏主界面初始化
def draw_init():
    bgm1()
    global playCG
    if not playCG:
        CG.PlayVideo()
        playCG = True
    click = False
    while True:
        screen.blit(game_img.init_bg_img, (-100, -250))
        draw_text(screen, '打飞机', 64, config.WIDTH / 2, config.HEIGHT / 4 - 100)
        mx, my = pg.mouse.get_pos()

        button_1_text = font.render("Free mode", True, (135, 206, 250))
        button_2_text = font.render("Help", True, (135, 206, 250))
        button_3_text = font.render("Store", True, (135, 206, 250))
        button_4_text = font.render("Login", True, (135, 206, 250))
        button_5_text = font.render("PVE MODE", True, (135, 206, 250))

        button_1_image = game_img.btn1_img
        button_1 = pg.Rect(50, 100, 200, 50)
        screen.blit(button_1_image, button_1)
        screen.blit(button_1_text, (button_1.x + 10, button_1.y + 20))

        button_2 = pg.Rect(50, 300, 200, 50)
        screen.blit(button_1_image, button_2)
        screen.blit(button_2_text, (button_2.x + 10, button_2.y + 20))

        button_3 = pg.Rect(50, 400, 200, 50)
        screen.blit(button_1_image, button_3)
        screen.blit(button_3_text, (button_3.x + 10, button_3.y + 20))

        button_4 = pg.Rect(50, 500, 200, 50)
        screen.blit(button_1_image, button_4)
        screen.blit(button_4_text, (button_4.x + 10, button_4.y + 20))

        button_5 = pg.Rect(50, 200, 200, 50)
        screen.blit(button_1_image, button_5)
        screen.blit(button_5_text, (button_5.x + 10, button_5.y + 20))

        if button_1.collidepoint((mx, my)):
            if click:
                game_main()
        if button_2.collidepoint((mx, my)):
            if click:
                help_()
        if button_3.collidepoint((mx, my)):
            if click:
                store()
        if button_4.collidepoint((mx, my)):
            if click and tk_login.is_logged_in is False:
                login()
            elif click and tk_login.is_logged_in is True:
                profile()
        if button_5.collidepoint((mx, my)):
            if click:
                chapter2()
        click = False

        # 取得输入
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pg.display.update()
        clock.tick(config.FPS)


connect_ = pymysql.connect(host="localhost", user="root", port=3307, password="Jason20040903", database="user_info",
                           charset="utf8")
bg1 = plane_sprite.BackGroud(False,
                             "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make/img/background.png")
bg2 = plane_sprite.BackGroud(True,
                             "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make/img/background.png")
back_group = pg.sprite.Group(bg1, bg2)
odds = 0
highest_score = 0

# 开启摄像头和显示的参数
cap: VideoCapture = cv2.VideoCapture(0)  # 开启摄像头
fontFace = cv2.FONT_HERSHEY_SIMPLEX
lineType = cv2.LINE_AA


# 游戏主体
def game_main():
    player.image = game_img.player_img
    health = player.health
    lives = player.lives
    player.rect.centerx = config.WIDTH / 2
    player.rect.bottom = config.HEIGHT - 10
    score = 0

    with mp_hands.Hands(model_complexity=0, max_num_hands=1, min_detection_confidence=0.55, static_image_mode=False,
                        min_tracking_confidence=0.55) as hands:
        if not cap.isOpened():
            tk.messagebox.showerror("警告", "打开摄像头失败")
            exit()

        running = True
        w, h = 600, 400  # 摄像头图像的尺寸

        while cap.isOpened() and running:
            ret, img = cap.read()
            img = cv2.flip(img, 1)
            if not ret:
                print("Cannot receive frame")
                break
            img = cv2.resize(img, (600, 350))  # 調整畫面尺寸
            size = img.shape  # 取得攝影機影像尺寸
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 將 BGR 轉換成 RGB
            results = hands.process(img2)  # 偵測手掌
            if results.multi_hand_landmarks:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                      results.multi_handedness):
                    label = handedness.classification[0].label
                    left_hand_landmarks = hand_landmarks
                    right_hand_landmarks = hand_landmarks
                    right_finger_points = []  # 储存手指的坐标
                    left_finger_points = []
                    x_1 = int(left_hand_landmarks.landmark[0].x * img.shape[1])  # 获取第 0 号关键点（手腕根部）的坐标
                    y_1 = int(left_hand_landmarks.landmark[0].y * img.shape[0])
                    x_2 = int(right_hand_landmarks.landmark[0].x * img.shape[1])  # 获取第 0 号关键点（手腕根部）的坐标
                    y_2 = int(right_hand_landmarks.landmark[0].y * img.shape[0])
                    for i in left_hand_landmarks.landmark:
                        x_ = i.x * w  # 这里乘w, h可以理解为线性变换
                        y_ = i.y * h
                        left_finger_points.append((x_, y_))
                    if left_finger_points:
                        finger_angle = ggf.hand_angle(left_finger_points)
                        text = ggf.gesture(finger_angle)
                        cv2.putText(img, text, (30, 120), fontFace, 5, (255, 255, 255), 10, lineType)
                    for i in right_hand_landmarks.landmark:
                        x_ = i.x * w  # 这里乘w, h可以理解为线性变换
                        y_ = i.y * h
                        right_finger_points.append((x_, y_))
                    if right_finger_points:
                        finger_angle = ggf.hand_angle(right_finger_points)
                        text = ggf.gesture(finger_angle)
                        cv2.putText(img, text, (30, 120), fontFace, 5, (255, 255, 255), 10, lineType)
                    # 显示出左右手
                    cv2.putText(img, f"{label}", (x_1, y_1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255),
                                2)
                    # 將節點和骨架繪製到影像中
                    mp_drawing.draw_landmarks(
                        img,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

                # 飞船移动
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                cx = int(wrist.x * w)
                cy = int(wrist.y * h)
                if cx > w / 2:
                    player.rect.x += player.speed
                elif cx < w / 2:
                    player.rect.x -= player.speed
                if cy > h / 2:
                    player.rect.y += player.speed
                elif cy < h / 2:
                    player.rect.y -= player.speed

                # 射击
                if player.image != game_img.player_img_min:
                    if ggf.gesture(finger_angle) == 'rock' and label == 'Left':
                        player.shoot_left()
                    if ggf.gesture(finger_angle) == 'rock' and label == 'Right':
                        player.shoot_right()

                # 缩小,还原
                if ggf.gesture(finger_angle) == 'scissor' and label == 'Left':
                    player.image = game_img.player_img_min
                elif ggf.gesture(finger_angle) == 'paper' and label == 'Left':
                    player.image = game_img.player_img
                if ggf.gesture(finger_angle) == 'scissor' and label == 'Right':
                    player.image = game_img.player_img_min
                elif ggf.gesture(finger_angle) == 'paper' and label == 'Right':
                    player.image = game_img.player_img

            cv2.imshow('test', img)
            if cv2.waitKey(5) == ord('q'):
                break  # 按下 q 鍵停止

            clock.tick(config.FPS)
            # 特殊反应
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit_game = tk.messagebox.askyesno("quit", "是否确认退出游戏，您在游戏中获得的积分将消失!")
                    if quit_game:
                        cv2.destroyAllWindows()
                        running = False
                    else:
                        pass
                if event.type == INVINCIBLE_TIME:
                    player.invincible = False  # 取消无敌状态
                    player.image = game_img.player_img
                pg.time.set_timer(INVINCIBLE_TIME, 0)  # 取消定时器

            # 更新
            all_sprites.update()

            # 子弹和陨石碰撞
            hits = pg.sprite.groupcollide(rocks, bullets, True, True)  # 后面两个参数是判断碰撞后要不要删除;返回值是字典；默认矩形碰撞判断
            for hit in hits:
                pg.mixer.Sound.play(random.choice(game_sound.expl_sounds))
                score += int(hit.radius)
                expl = Exploration(hit.rect.center, 'big')
                all_sprites.add(expl)
                # 掉宝机率
                if random.random() > 0.85 - odds:
                    pow = Power(hit.rect.center)
                    all_sprites.add(pow)
                    # powers = pg.sprite.Group() 这个地方加上去就在发射时吃不到道具了，因为创建了一个新的精灵模组，飞机只能和最后的发生互动
                    powers.add(pow)
                new_rock()

            # 激光碰撞陨石
            hits = pg.sprite.groupcollide(rocks, lasers, True, False)  # 后面两个参数是判断碰撞后要不要删除;返回值是字典；默认矩形碰撞判断
            for hit in hits:
                pg.mixer.Sound.play(random.choice(game_sound.expl_sounds))
                score += int(hit.radius)
                expl = Exploration(hit.rect.center, 'big')
                all_sprites.add(expl)
                # 掉宝机率
                if random.random() > 0.85 - odds:
                    pow = Power(hit.rect.center)
                    all_sprites.add(pow)
                    # powers = pg.sprite.Group() 这个地方加上去就在发射时吃不到道具了，因为创建了一个新的精灵模组，飞机只能和最后的发生互动
                    powers.add(pow)
                new_rock()

            # 飞机和陨石碰撞
            hits = pg.sprite.spritecollide(player, rocks, True, pg.sprite.collide_circle)  # 需要在类中加radius
            for hit in hits:
                expl = Exploration(hit.rect.center, 'small')
                all_sprites.add(expl)
                if not player.invincible:
                    health -= int(hit.radius)
                # print(player.health)
                new_rock()
                if health <= 0:
                    death = Death(player.rect.center)
                    pg.mixer.Sound.play(game_sound.die_sound)
                    all_sprites.add(death)
                    health = player.health
                    lives -= 1
                    # print(player.lives)
                    player.hide()
            if lives == 0 and not (death.alive()):
                if tk_login.is_logged_in:
                    cursor = connect_.cursor()
                    cursor.execute('use user_info')
                    sql_take = "SELECT highest_record FROM user_base_info WHERE user_name = %s"
                    cursor.execute(sql_take, (tk_login.user_name))
                    row = cursor.fetchone()
                    table_highest_score = row[0]
                    global highest_score
                    if table_highest_score < score:
                        highest_score = score
                    sql_record = "UPDATE user_base_info SET highest_record = %s WHERE user_name = %s"
                    cursor.execute(sql_record, (highest_score, tk_login.user_name))
                    sql_in = "UPDATE user_base_info SET score = score + %s WHERE user_name = %s"
                    cursor.execute(sql_in, (score, tk_login.user_name))
                    connect_.commit()
                draw_text(screen, '你失败了', 26, config.WIDTH / 2, 50)
                draw_text(screen, '按任意键继续', 26, config.WIDTH / 2, 100)
                pg.mixer.Sound.play(game_sound.die_music)
                pg.display.update()
                waiting = True  # 设置一个等待标志
                while waiting:  # 进入一个等待循环
                    for event in pg.event.get():
                        if event.type == pg.KEYUP:  # 如果检测到用户按下任意键
                            waiting = False  # 结束等待循环
                            cv2.destroyAllWindows()
                            return  # 跳出game_main函数
                        if event.type == pg.QUIT:
                            cv2.destroyAllWindows()
                            running = False
                            return

            # 飞机和宝物碰撞
            hits = pg.sprite.spritecollide(player, powers, True)
            for hit in hits:
                if hit.type == 'shield':
                    pg.mixer.Sound.play(game_sound.shield_sound)
                    health += 10
                    if health >= player.health:
                        health = player.health
                if hit.type == 'gun':
                    pg.mixer.Sound.play(game_sound.gun_sound)
                    player.gunup()
                if hit.type == 'time':
                    pg.mixer.Sound.play(game_sound.time_sound)
                    player.invincible_time()
                if hit.type == 'time2':
                    pg.mixer.Sound.play(game_sound.time_2_sound)
                    score = int(score) * 2

            back_group.draw(screen)
            # screen.blit(game_img.background_img, (0, 0))  # 显示背景图片的方法
            all_sprites.draw(screen)
            draw_text(screen, str(score), 18, config.WIDTH / 2, 10)
            draw_health(screen, health, 10, 10, str(health), 18, config.RED)
            if lives <= 3:
                draw_lives(screen, lives, game_img.player_lives_img, config.WIDTH - 100, 15)
            else:
                draw_lives(screen, lives, game_img.player_lives_img, config.WIDTH - 180, 15)

            # 更新画面
            back_group.update()
            pg.display.update()


# 游戏帮助说明
def help_():
    while True:
        screen.blit(game_img.help_bg, (0, -200))  # 显示图片的方法
        draw_text(screen, '新手教程', 64, config.WIDTH / 2, config.HEIGHT / 4 - 100)
        draw_text(screen, '使用手掌移动飞船\n左手握拳发射激光\n右手握拳发射子弹', 26, config.WIDTH / 2,
                  config.HEIGHT / 4 + 100)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return draw_init()
        pg.display.update()
        clock.tick(config.FPS)


n_1, n_2, n_3, n_4 = 0, 0, 0, 0  # n 等於 0
num_font = pg.font.SysFont('Arial', 32)


# 定义一个函数来绘制数字在屏幕上
def draw_num(screen, num, x, y):
    # 渲染数字为文字图片
    num_text = num_font.render("Level:" + str(num), True, (255, 0, 0), (0, 0, 0))
    # 绘制文字图片到屏幕上
    screen.blit(num_text, (x, y))


# 商店系统
def store():
    click = False
    while True:
        global n_1, n_2, n_3, n_4
        screen.blit(game_img.store_img, (0, -200))  # 显示图片的方法
        draw_text(screen, '商店', 64, config.WIDTH / 2, config.HEIGHT / 4 - 100)
        mx, my = pg.mouse.get_pos()
        button_1_text = font_zh.render("增加掉落机率(max10)", True, (135, 206, 250))
        button_2_text = font_zh.render("增加飞船移动速度(max10)", True, (135, 206, 250))
        button_3_text = font_zh.render("增加生命条数(max3)", True, (135, 206, 250))
        button_4_text = font_zh.render("增加生命值上限(max10)", True, (135, 206, 250))

        button_1_image = game_img.btn1_img
        button_1 = pg.Rect(50, 110, 200, 50)
        screen.blit(button_1_image, button_1)
        screen.blit(button_1_text, (button_1.x + 10, button_1.y + 20))

        button_2 = pg.Rect(50, 210, 200, 50)
        screen.blit(button_1_image, button_2)
        screen.blit(button_2_text, (button_2.x + 10, button_2.y + 20))

        button_3 = pg.Rect(50, 310, 200, 50)
        screen.blit(button_1_image, button_3)
        screen.blit(button_3_text, (button_3.x + 10, button_3.y + 20))

        button_4 = pg.Rect(50, 410, 200, 50)
        screen.blit(button_1_image, button_4)
        screen.blit(button_4_text, (button_4.x + 10, button_4.y + 20))

        if button_1.collidepoint((mx, my)):
            if click:
                n_1 += 1
                global odds
                odds += 0.01
        if button_2.collidepoint((mx, my)):
            if click:
                n_2 += 1
                player.speed += 0.1
        if button_3.collidepoint((mx, my)):
            if click:
                n_3 += 1
                player.lives += 1
        if button_4.collidepoint((mx, my)):
            if click:
                n_4 += 1
                player.health += 10
        click = False

        draw_num(screen, n_1, 400, 120)
        draw_num(screen, n_2, 400, 220)
        draw_num(screen, n_3, 400, 320)
        draw_num(screen, n_4, 400, 420)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return draw_init()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pg.display.update()
        clock.tick(config.FPS)


# 登录系统
def login():
    main = tk_login.My_Gui()
    main.set_init_window()


def profile():
    main = User_Gui()
    main.set_init_window()


class User_Gui():
    def __init__(self):
        self.main_screen = tk.Tk()

    def set_init_window(self):
        self.main_screen.geometry('600x500')
        self.main_screen.resizable(False, False)
        self.main_screen.title('user')

        canvas = tk.Canvas(self.main_screen, width=1000, height=1000)
        # 图片
        image_ = Image.open(
            'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/login_bg.gif')
        image_bg = ImageTk.PhotoImage(image_)
        image = canvas.create_image(100, 0, anchor='n', image=image_bg)
        canvas.pack()
        tk.Label(self.main_screen, text='欢迎回到飞机大战', font=('宋体', 20), fg="blue", bg='Light Sea Green',
                 relief=SUNKEN).place(x=200,
                                      y=20)
        tk.Label(self.main_screen, text='用户:' + tk_login.user_name, font=('宋体', 20), fg="blue",
                 bg='Light Sea Green',
                 relief=SUNKEN).place(x=200,
                                      y=50)
        # 用户获得的总分
        cur = connect_.cursor()
        sql = "SELECT score,highest_record FROM user_base_info WHERE user_name = %s"
        cur.execute(sql, (tk_login.user_name))
        row = cur.fetchone()
        score = row[0]
        ht_score = row[1]
        tk.Label(self.main_screen, text="您的总分数为：" + str(score) + "\n您的最高得分为：" + str(ht_score),
                 font=('宋体', 20), fg="blue",
                 bg='Light Sea Green', relief=SUNKEN).place(x=200, y=80)

        # 设置头像，统一头像，或用户存入的头像
        user_img = Image.open(
            'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/user_img_100x100.jpg')
        user_tk_img = ImageTk.PhotoImage(user_img)
        canvas_ = tk.Canvas(self.main_screen, width=90, height=90)  # 设置头像画布的宽度和高度为100
        canvas_.create_image(0, 0, anchor='nw', image=user_tk_img)  # 在 Canvas 中放入圖片
        canvas_.place(x=50, y=50)  # 设置头像画布的位置为左上角

        # 退出按钮
        btn_quit = tk.Button(self.main_screen, text='登出', width=10, height=1, activebackground="RoyalBlue",
                             relief=RIDGE, command=lambda: self.quit_in(),
                             bg="Cyan")
        btn_quit.place(x=250, y=400)

        self.main_screen.mainloop()

        # 更换头像（选做）

    def quit_in(self):
        tk.messagebox.showinfo("提示", "登出成功！")
        self.main_screen.destroy()
        self.main_screen.quit()
        tk_login.is_logged_in = False


# chapter2
game_window = pg.display.set_mode(SIZE)
pg.display.set_caption("chapter2")

player_image = pg.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/game_sprite/player.png")
boss_image = pg.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/boss.png")
boss_image = pg.transform.scale(boss_image, (230, 230))
enemy_bullet_image = pg.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/game_sprite/enemy_bullet.png")
enemy_bullet_image = pg.transform.scale(enemy_bullet_image, (40, 40))
laser_image = pg.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/game_sprite/laser.png")
enemy_image = pg.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/game_sprite/enemy.png")

# Define game colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (0, 255, 255)

# Define enemy properties
enemy_width = 70
enemy_height = 70
enemy_speed = 3
enemy_spawn_delay = 60
enemy_bullet_speed = 5
enemy_fire_delay = 60

# Set up game clock
clock = pg.time.Clock()

# Define game variables
score = 0
game_over = False
enemies_spawned = 0
enemies_to_spawn = 10
level = 1

# Define boss variables
boss_health = 1000
boss_attack_delay = 60
boss_bullet_speed = 10
boss_laser_delay = 240
laser_speed = 3

# Define bullet properties
bullet_width = 20
bullet_height = 35
bullet_speed = 10

# Create lists for bullets and enemies
player_bullets = []
enemies = []
enemy_bullets = []
boss_lasers = []
items = []

# 完全组
ch2_all_sprites = pg.sprite.Group()


class PlayerCh2(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = player_image
        self.rect = self.image.get_rect()
        # 用来设置回到原点
        self.rect.centerx = config.WIDTH / 2
        self.rect.bottom = config.HEIGHT - 10
        self.speed = 5
        self.lives = 3
        self.health = 100
        self.invisible = False
        self.player_invisible_delay_time = 120
        self.player_flash_delay = 20

    def update(self):
        if self.rect.right > WINDOWWIDTH:
            self.rect.right = WINDOWWIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > WINDOWHEIGHT:
            self.rect.bottom = WINDOWHEIGHT
        if self.rect.top < 0:
            self.rect.top = 0


# player对象
playerCh2 = PlayerCh2()

# boss 精灵——Rect类型
boss_sprite = pg.Rect(200, 100, 300, 120)


def create_enemy():
    # Create a new enemy sprite
    enemy_x = random.randint(0, WINDOWWIDTH - enemy_width)
    enemy_y = 0 - enemy_height
    enemy_sprite = pg.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    enemies.append(enemy_sprite)
    # print("Enemy spawned, total enemies: ", len(enemies))


def create_enemy_bullet(enemy):
    # Create a new enemy bullet sprite
    bullet_x = enemy.centerx - bullet_width / 2
    bullet_y = enemy.bottom
    bullet_sprite = pg.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
    enemy_bullets.append(bullet_sprite)


def update_enemies():
    # Move and remove enemies that have gone offscreen
    global game_over
    for enemy in enemies:
        enemy.move_ip(0, enemy_speed)
        if enemy.top > WINDOWHEIGHT:
            enemies.remove(enemy)
            # global player_lives
            # player_lives -= 1
            # if player_lives == 0:
            #     global game_over
            #     game_over = True
            # else:
            #     # Make the player briefly invisible if they have just lost a life
            #     global player_invisible, player_invisible_delay
            #     player_invisible = True
            #     player_invisible_delay = 120
            # player_sprite.bottom = -100

        # Randomly fire bullets
        global enemy_fire_delay
        enemy_fire_delay -= 1
        if enemy_fire_delay == 0 and not enemy.colliderect(playerCh2.rect):
            create_enemy_bullet(enemy)
            enemy_fire_delay = 60
        if not playerCh2.invisible:
            if playerCh2.rect.colliderect(enemy):
                pg.mixer.Sound.play(random.choice(game_sound.expl_sounds))
                expl = Exploration(enemy.center, 'small')
                ch2_all_sprites.add(expl)
                enemies.remove(enemy)
                if playerCh2.lives == 0:
                    game_over = True
                else:
                    pass
                    # Make the player briefly invisible if they have just lost a life
                    # playerCh2.invisible = True
                    # playerCh2.player_invisible_delay = playerCh2.player_invisible_delay_time
                # player_sprite.bottom = -100


def update_enemy_bullets():
    # Move and remove enemy bullets that have gone offscreen
    for bullet in enemy_bullets:
        bullet.move_ip(0, enemy_bullet_speed)
        if bullet.top > WINDOWHEIGHT:
            enemy_bullets.remove(bullet)


def create_boss():
    global boss_sprite, boss_health, boss_attack_delay, boss_bullet_speed
    boss_sprite = pg.Rect(200, 100, 300, 120)
    boss_health = 1000
    boss_attack_delay = 60
    boss_bullet_speed = 10


def create_boss_bullet():
    # Create a new boss bullet sprite
    bullet_x = boss_sprite.centerx - bullet_width / 2
    bullet_y = boss_sprite.bottom
    bullet_sprite = pg.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
    enemy_bullets.append(bullet_sprite)


def check_boss_collisions():
    # Check for collisions between player bullets and the boss
    global boss_health
    for bullet in enemy_bullets:
        if not playerCh2.invisible:
            if bullet.colliderect(playerCh2.rect):
                expl = Exploration(bullet.center, 'small')
                ch2_all_sprites.add(expl)
                enemy_bullets.remove(bullet)
                playerCh2.health -= 10
                if playerCh2.health <= 0:
                    playerCh2.health = 100
                    playerCh2.lives -= 1
                else:
                    pass
                    # Make the player briefly invisible if they have just lost a life
                    # playerCh2.invisible = True
                    # playerCh2.player_flash_delay = playerCh2.player_invisible_delay_time
                    # player_sprite.bottom = -100


def create_boss_laser():
    # Create a new laser sprite
    laser_width = 100
    laser_height = 150
    laser_x = boss_sprite.centerx - laser_width / 2
    laser_y = boss_sprite.bottom
    laser_sprite = pg.Rect(laser_x, laser_y, laser_width, laser_height)
    pg.mixer.Sound.play(game_sound.boss_laser_sound)
    boss_lasers.append(laser_sprite)


def update_boss():
    global boss_sprite, boss_health, boss_attack_delay, boss_bullet_speed, game_over
    if boss_health > 0:
        # Move the boss around randomly
        boss_sprite.move_ip(random.randint(-12, 13), random.randint(-13, 12))
        # Prevent the boss from going out of the game window
        if boss_sprite.left < 0:
            boss_sprite.left = 0
        if boss_sprite.right > WINDOWWIDTH:
            boss_sprite.right = WINDOWWIDTH
        if boss_sprite.top < 0:
            boss_sprite.top = 0
        if boss_sprite.bottom > WINDOWHEIGHT:
            boss_sprite.bottom = WINDOWHEIGHT
        # Fire bullets at the player
        boss_attack_delay -= 1
    if boss_attack_delay == 0:
        create_boss_bullet()
        boss_attack_delay = 30

    global boss_laser_delay, laser_speed
    boss_laser_delay -= 1
    if boss_laser_delay == 0:
        create_boss_laser()
        # print (boss_laser_delay)
        boss_laser_delay = 240

    if not playerCh2.invisible:
        if playerCh2.rect.colliderect(boss_sprite):
            # Move the boss away from the player
            if boss_sprite.centerx < playerCh2.rect.centerx:
                boss_sprite.move_ip(-10, 0)
            else:
                boss_sprite.move_ip(10, 0)
            if boss_sprite.centery < playerCh2.rect.centery:
                boss_sprite.move_ip(0, -10)
            else:
                boss_sprite.move_ip(0, 10)
            playerCh2.health -= 1
            if playerCh2.health == 0:
                playerCh2.health = 100
                playerCh2.lives -= 1
            else:
                pass
                # Make the player briefly invisible if they have just lost a life
                # playerCh2.invisible = True
                # playerCh2.player_flash_delay = playerCh2.player_invisible_delay_time
                # player_sprite.bottom = -100

    for laser in boss_lasers:
        laser.move_ip(0, laser_speed)
        if not playerCh2.invisible:
            if laser.colliderect(playerCh2.rect):
                boss_laser_delay = 240
                playerCh2.health -= 10
                if playerCh2.health == 0:
                    playerCh2.health = 100
                    if playerCh2.lives != 0:
                        playerCh2.lives -= 1
                    else:
                        game_over = True
                else:
                    pass
                    # Make the player briefly invisible if they have just lost a life
                    # playerCh2.invisible = True
                    # playerCh2.player_invisible_delay = playerCh2.player_invisible_delay_time
        if laser.bottom < 0:
            boss_lasers.remove(laser)


flag = False


def draw_game():
    font = pg.font.Font(None, 36)
    boss_health_text = font.render("Boss Health: " + str(boss_health), True, config.WHITE)
    draw_health(game_window, boss_health, 150, 40, str(boss_health), 24, blue)
    # game_window.blit(boss_health_text, (WINDOWWIDTH / 2 - 70, 50))
    game_window.blit(boss_image, boss_sprite)
    for enemy in enemies:
        game_window.blit(enemy_image, enemy)


def bgm2():
    # 音乐
    pg.mixer.music.load(
        'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/background_music.mp3')
    pg.mixer.music.set_volume(0.5)
    pg.mixer.music.play(-1)


def create_level():
    global level, enemy_speed, enemy_fire_delay, enemy_spawn_delay, enemies_spawned, enemies_to_spawn, enemy_bullet_speed
    level += 1
    enemy_speed += 2
    enemy_fire_delay -= 10
    enemy_spawn_delay = 50
    enemies_spawned = 0
    enemies_to_spawn += 10
    enemy_bullet_speed += 2


def create_level_2():
    global boss_image
    boss_image = pg.image.load(
        "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/boss_level_2-removebg-preview.png")
    boss_image = pg.transform.scale(boss_image, (230, 230))


def create_level_3():
    pass


def update_game_ch2():
    ch2_all_sprites.update()
    update_enemies()
    update_enemy_bullets()
    check_boss_collisions()
    back_group.update()
    playerCh2.update()
    update_boss()
    if (level == 1) and (enemies_spawned > 50):
        create_level()
    if (level == 2) and (enemies_spawned > 50):
        create_level_2()
    if (level == 3) and (enemies_spawned > 75):
        pass


def chapter2():
    # 背景音乐
    bgm2()
    global enemies_spawned, enemies_to_spawn, level, enemy_spawn_delay, background_speed
    playerCh2.lives = 3
    playerCh2.health = 100
    flag_ = True
    connect_ = pymysql.connect(host="localhost", user="root", port=3307, password="Jason20040903", database="user_info",
                               charset="utf8")
    background_image = pg.image.load(
        "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/chapter2_bg.jpg")
    background_rect = background_image.get_rect()

    background_surface = pg.Surface((800, 3200))
    for x in range(0, 600, background_image.get_width()):
        for y in range(0, 3200, background_image.get_height()):
            background_surface.blit(background_image, (x, y))
    background_position = [0, -WINDOWHEIGHT]

    playerCh2.rect.centerx = config.WIDTH / 2
    playerCh2.rect.bottom = config.HEIGHT - 10
    score = 0

    with mp_hands.Hands(model_complexity=0, max_num_hands=1, min_detection_confidence=0.55, static_image_mode=False,
                        min_tracking_confidence=0.55) as hands:
        if not cap.isOpened():
            tk.messagebox.showerror("警告", "打开摄像头失败")
            exit()

        run = True  # 設定是否更動觸碰區位置
        running = True
        show_init = True
        w, h = 600, 400  # 图像的尺寸

        while cap.isOpened() and running:
            health = playerCh2.health
            lives = playerCh2.lives
            ret, img = cap.read()
            img = cv2.flip(img, 1)
            if not ret:
                print("Cannot receive frame")
                break
            img = cv2.resize(img, (600, 350))  # 調整畫面尺寸
            size = img.shape  # 取得攝影機影像尺寸
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 將 BGR 轉換成 RGB
            results = hands.process(img2)  # 偵測手掌
            if results.multi_hand_landmarks:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                      results.multi_handedness):
                    label = handedness.classification[0].label
                    left_hand_landmarks = hand_landmarks
                    right_hand_landmarks = hand_landmarks
                    right_finger_points = []  # 储存手指的坐标
                    left_finger_points = []
                    x_1 = int(left_hand_landmarks.landmark[0].x * img.shape[1])  # 获取第 0 号关键点（手腕根部）的坐标
                    y_1 = int(left_hand_landmarks.landmark[0].y * img.shape[0])
                    x_2 = int(right_hand_landmarks.landmark[0].x * img.shape[1])  # 获取第 0 号关键点（手腕根部）的坐标
                    y_2 = int(right_hand_landmarks.landmark[0].y * img.shape[0])
                    for i in left_hand_landmarks.landmark:
                        x_ = i.x * w  # 这里乘w, h可以理解为线性变换
                        y_ = i.y * h
                        left_finger_points.append((x_, y_))
                    if left_finger_points:
                        finger_angle = ggf.hand_angle(left_finger_points)
                        text = ggf.gesture(finger_angle)
                        cv2.putText(img, text, (30, 120), fontFace, 5, (255, 255, 255), 10, lineType)
                    for i in right_hand_landmarks.landmark:
                        x_ = i.x * w  # 这里乘w, h可以理解为线性变换
                        y_ = i.y * h
                        right_finger_points.append((x_, y_))
                    if right_finger_points:
                        finger_angle = ggf.hand_angle(right_finger_points)
                        text = ggf.gesture(finger_angle)
                        cv2.putText(img, text, (30, 120), fontFace, 5, (255, 255, 255), 10, lineType)
                    # 显示出左右手
                    cv2.putText(img, f"{label}", (x_1, y_1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255),
                                2)
                    # 將節點和骨架繪製到影像中
                    mp_drawing.draw_landmarks(
                        img,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

                # 飞船移动
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                cx = int(wrist.x * w)
                cy = int(wrist.y * h)
                # right
                if cx > w / 2:
                    playerCh2.rect.x += playerCh2.speed
                # left
                elif cx < w / 2:
                    playerCh2.rect.x -= playerCh2.speed
                # bottom
                if cy > h / 2:
                    playerCh2.rect.y += playerCh2.speed
                # top
                elif cy < h / 2:
                    playerCh2.rect.y -= playerCh2.speed

                # # 射击
                # if ggf.gesture(finger_angle) == 'rock' and label == 'Left':
                #     player.shoot_left()
                # if ggf.gesture(finger_angle) == 'rock' and label == 'Right':
                #     player.shoot_right()

            cv2.imshow('test', img)
            if cv2.waitKey(5) == ord('q'):
                break  # 按下 q 鍵停止

            # 特殊反应
            for event in pg.event.get():
                # 回到主页
                if event.type == pg.QUIT:
                    quit_game = tk.messagebox.askyesno("quit", "是否确认退出游戏，您在游戏中获得的积分将消失!")
                    if quit_game:
                        pg.mixer.music.stop()
                        cv2.destroyAllWindows()
                        bgm1()
                        running = False
                    else:
                        pass
                # 无敌状态
                # if event.type == INVINCIBLE_TIME:
                #     player.invincible = False  # 取消无敌状态
                #     player.image = game_img.player_img
                # pg.time.set_timer(INVINCIBLE_TIME, 0)  # 取消定时器

            background_position[1] += 1
            if background_position[1] > 0:
                background_position[1] -= 1600
            game_window.blit(background_surface, background_position)
            draw_text(game_window, "score:" + str(score), 24, config.WIDTH / 2 + 100, 10)
            level_text = font.render("Level: " + str(level), True, white)
            game_window.blit(level_text, (WINDOWWIDTH / 2 - 50, 10))
            draw_health(game_window, health, 10, 10, str(health), 18, config.RED)
            for bullet in enemy_bullets:
                # pygame.draw.rect(game_window, red, bullet)
                game_window.blit(enemy_bullet_image, bullet)
            for laser in boss_lasers:
                game_window.blit(laser_image, laser)
            if lives <= 3:
                draw_lives(game_window, lives, game_img.player_lives_img, config.WIDTH - 100, 15)
            else:
                draw_lives(game_window, lives, game_img.player_lives_img, config.WIDTH - 180, 15)

            enemy_spawn_delay -= 1
            if (enemy_spawn_delay == 0):
                create_enemy()
                if level == 2:
                    enemy_spawn_delay = 50
                else:
                    enemy_spawn_delay = 60
                enemies_spawned += 1

            # 更新画面
            ch2_all_sprites.draw(game_window)
            check_boss_collisions()
            if flag_:
                create_boss()
                flag_ = False
            draw_game()
            game_window.blit(player_image, playerCh2)
            update_game_ch2()
            pg.display.update()
            clock.tick(config.FPS)


# 运行
# draw_init()
chapter2()

# 退出
pg.quit()
cap.release()
cv2.destroyAllWindows()
sys.exit()
