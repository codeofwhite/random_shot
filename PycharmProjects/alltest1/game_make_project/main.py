import sys
import cv2
import mediapipe as mp
import pygame as pg
import random
import config
import gesture.gesture_funcs as ggf
import game.game_sounds as game_sound
import game.game_imgs as game_img
from pygame.locals import *

# 初始化
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((config.WIDTH, config.HEIGHT))
# 更改caption
pg.display.set_caption("打飞机")
pg.display.set_icon(pg.image.load('C:/Users/zhj20/PycharmProjects/alltest1/game_make/img/player.png'))
clock = pg.time.Clock()

# 手势初始化
mp_drawing = mp.solutions.drawing_utils  # mediapipe 繪圖方法
mp_drawing_styles = mp.solutions.drawing_styles  # mediapipe 繪圖樣式
mp_hands = mp.solutions.hands  # mediapipe 偵測手掌方法


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(game_img.player_img, (50, 38))
        self.image.set_colorkey(config.BLACK)  # 黑色变透明
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

    def update(self):
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
            if current_time - self.last_shot_time >= 200:
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
            if current_time - self.last_shot_time >= 1000:
                if self.gun == 1:
                    laser = Laser(self.rect.centerx, self.rect.top)
                    all_sprites.add(laser)
                    lasers.add(laser)
                    self.last_shot_time = current_time
                    pg.mixer.Sound.play(game_sound.laser_sound)

    def hide(self):
        self.hidden = True
        self.hide_time = pg.time.get_ticks()
        print('hide')

    def gunup(self):
        if not self.hidden:
            self.gun += 1
            self.gun_time = pg.time.get_ticks()


class Rock(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(game_img.rock_imgs)
        self.image = pg.Surface((50, 50))
        self.image = self.image_ori.copy()
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()  # 外面的框
        # pg.draw.rect(self.image, RED, self.rect)
        self.radius = self.rect.width * 0.85 / 2
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, config.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -110)
        self.speedy = random.randrange(1, 9)
        self.speedx = random.randrange(-5, 5)
        self.total_degree = 0
        self.rot_degree = random.randrange(-2, 5)

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


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = game_img.bullet_img
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()  # 外面的框
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Laser(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = game_img.laser_img
        self.image.set_colorkey(config.BLACK)
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


class Power(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = game_img.power_imgs[self.type]
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()  # 外面的框
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y >= config.HEIGHT:
            self.kill()


player = Player()
bullets = pg.sprite.Group()
rocks = pg.sprite.Group()
powers = pg.sprite.Group()
lasers = pg.sprite.Group()
all_sprites = pg.sprite.Group()
all_sprites.add(player)
for i in range(8):
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)
pg.mixer.music.play(-1)
score = 0

cap = cv2.VideoCapture(0)  # 开启摄像头
fontFace = cv2.FONT_HERSHEY_SIMPLEX
lineType = cv2.LINE_AA


def draw_text(surf, text, size, x, y):
    font = pg.font.Font(game_img.font_name, size)
    text_surface = font.render(text, True, config.WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)


def draw_health(surf, hp, x, y, text, size):
    if hp <= 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = hp / 100 * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, config.RED, fill_rect)  # 血条
    pg.draw.rect(surf, config.WHITE, outline_rect, 2)  # 血条外框
    font = pg.font.Font(game_img.font_name, size)
    text_surface = font.render(text, True, config.WHITE)
    text_rect = text_surface.get_rect()
    text_rect.x = BAR_LENGTH / 2
    text_rect.y = y
    surf.blit(text_surface, text_rect)


def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i  # 间隔像素
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_init():
    screen.fill((0, 0, 0))
    draw_text(screen, '打飞机', 64, config.WIDTH / 2, config.HEIGHT / 4 - 100)
    draw_text(screen, '↑↓←→移动飞船，space发射子弹', 20, config.WIDTH / 2, config.HEIGHT / 4 + 100)
    draw_text(screen, '任意键开始游戏', 18, config.WIDTH / 2, config.HEIGHT / 4 + 300)
    pg.display.update()

    waiting = True
    while waiting:
        clock.tick(config.FPS)  # 一秒跑十次
        # 取得输入
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            if event.type == pg.KEYUP:
                waiting = False
                return False


def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)


with mp_hands.Hands(model_complexity=0, max_num_hands=2, min_detection_confidence=0.5, static_image_mode=False,
                    min_tracking_confidence=0.5) as hands:
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    run = True  # 設定是否更動觸碰區位置
    running = True
    show_init = True
    w, h = 540, 310  # 图像的尺寸

    while cap.isOpened() and running:
        if show_init:
            if draw_init():
                break
            all_sprites = pg.sprite.Group()
            rocks = pg.sprite.Group()
            bullets = pg.sprite.Group()
            powers = pg.sprite.Group()
            player = Player()
            all_sprites.add(player)
            for i in range(8):
                rock = Rock()
                all_sprites.add(rock)
                rocks.add(rock)
            score = 0
            draw_init()
            show_init = False
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        if not ret:
            print("Cannot receive frame")
            break
        img = cv2.resize(img, (540, 310))  # 調整畫面尺寸
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
            cx = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * w)
            cy = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * h)
            if cx > w / 2:
                player.rect.x += player.speed
            elif cx < w / 2:
                player.rect.x -= player.speed
            if cy > h / 2:
                player.rect.y += player.speed
            elif cy < h / 2:
                player.rect.y -= player.speed

            # 射击
            if ggf.gesture(finger_angle) == 'rock' and label == 'Left':
                player.shoot_left()
            if ggf.gesture(finger_angle) == 'rock' and label == 'Right':
                player.shoot_right()

        cv2.imshow('test', img)
        if cv2.waitKey(5) == ord('q'):
            break  # 按下 q 鍵停止

        clock.tick(config.FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # 更新
        all_sprites.update()

        # 子弹和陨石碰撞
        hits = pg.sprite.groupcollide(rocks, bullets, True, True)  # 后面两个参数是判断碰撞后要不要删除;返回值是字典；默认矩形碰撞判断
        for hit in hits:
            pg.mixer.Sound.play(random.choice(game_sound.expl_sounds))
            score += int(hit.radius)
            expl = Exploration(hit.rect.center, 'big')
            all_sprites.add(expl)
            if random.random() > 0.9:
                pow = Power(hit.rect.center)
                all_sprites.add(pow)
                # powers = pg.sprite.Group() 这个地方加上去就在发射时吃不到道具了，因为创建了一个新的精灵模组，飞机只能和最后的发生互动
                powers.add(pow)
            new_rock()

        # 子弹和激光碰撞
        hits = pg.sprite.groupcollide(rocks, lasers, True, False)  # 后面两个参数是判断碰撞后要不要删除;返回值是字典；默认矩形碰撞判断
        for hit in hits:
            pg.mixer.Sound.play(random.choice(game_sound.expl_sounds))
            score += int(hit.radius)
            expl = Exploration(hit.rect.center, 'big')
            all_sprites.add(expl)
            if random.random() > 0.9:
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
            player.health -= int(hit.radius)
            # print(player.health)
            new_rock()
            if player.health <= 0:
                death = Death(player.rect.center)
                pg.mixer.Sound.play(game_sound.die_sound)
                all_sprites.add(death)
                player.health = 100
                player.lives -= 1
                # print(player.lives)
                player.hide()
        if player.lives == 0 and not (death.alive()):
            # print('you lost')
            show_init = True

        # 飞机和宝物碰撞
        hits = pg.sprite.spritecollide(player, powers, True)
        for hit in hits:
            if hit.type == 'shield':
                pg.mixer.Sound.play(game_sound.shield_sound)
                player.health += 10
                if player.health >= 100:
                    player.health = 100
            if hit.type == 'gun':
                pg.mixer.Sound.play(game_sound.gun_sound)
                player.gunup()

        screen.blit(game_img.background_img, (0, 0))  # 显示图片的方法
        all_sprites.draw(screen)
        draw_text(screen, str(score), 18, config.WIDTH / 2, 10)
        draw_health(screen, player.health, 10, 10, str(player.health), 18)
        draw_lives(screen, player.lives, game_img.player_lives_img, config.HEIGHT - 190, 15)

        # 更新画面
        pg.display.update()

# 退出
pg.quit()
cap.release()
cv2.destroyAllWindows()
