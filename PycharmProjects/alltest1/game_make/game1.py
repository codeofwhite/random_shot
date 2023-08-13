'''
这个xy中的y轴是反的
'''
import time
import pygame as pg
import random
import os

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WIDTH = 500
HEIGHT = 600
FPS = 216

# 初始化
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
# 更改caption
pg.display.set_caption("打飞机")
pg.display.set_icon(pg.image.load('C:/Users/zhj20/PycharmProjects/alltest1/game_make/img/player.png'))
clock = pg.time.Clock()

# 载入图片
background_img = pg.image.load('C:/Users/zhj20/PycharmProjects/alltest1/game_make/img/background.png').convert()
player_img = pg.image.load('C:/Users/zhj20/PycharmProjects/alltest1/game_make/img/player.png').convert()
rock_img = pg.image.load('C:/Users/zhj20/PycharmProjects/alltest1/game_make/img/rock.png').convert()
bullet_img = pg.image.load('C:/Users/zhj20/PycharmProjects/alltest1/game_make/img/bullet.png').convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pg.image.load(f'C:/Users/zhj20/PycharmProjects/alltest1/game_make/img/rock{i}.png'))

font_name = pg.font.match_font('华文行楷')
# 爆炸动画要用图片
expl_anim = {}
expl_anim['big'] = []
expl_anim['small'] = []
for i in range(9):
    expl_img = pg.image.load(f'C:/Users/zhj20/PycharmProjects/alltest1/game_make/img/expl{i}.png').convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['big'].append(pg.transform.scale(expl_img, (75, 75)))
    expl_anim['small'].append(pg.transform.scale(expl_img, (50, 50)))
# 飞船死亡动画
player_expl_img = []
for i in range(9):
    expl_img = pg.image.load(f'C:/Users/zhj20/PycharmProjects/alltest1/game_make/img/player_expl{i}.png').convert()
    expl_img.set_colorkey(BLACK)
    player_expl_img.append(expl_img)
# 生命数
player_lives_img = pg.image.load(f'C:/Users/zhj20/PycharmProjects/alltest1/game_make/img/player.png')
player_lives_img = pg.transform.scale(player_lives_img, (20, 20))
player_lives_img.set_colorkey(BLACK)
# 石头掉落
power_imgs = {}
power_imgs['shield'] = pg.image.load(f'C:/Users/zhj20/PycharmProjects/alltest1/game_make/img/shield.png')
power_imgs['gun'] = pg.image.load(f'C:/Users/zhj20/PycharmProjects/alltest1/game_make/img/gun.png')

# 音乐
shoot_sound = pg.mixer.Sound('C:/Users/zhj20/PycharmProjects/alltest1/game_make/sound/shoot.wav')
expl_sounds = []
for i in range(2):
    expl_sounds.append(pg.mixer.Sound(f'C:/Users/zhj20/PycharmProjects/alltest1/game_make/sound/expl{i}.wav'))
# 背景音乐
BGM = pg.mixer.music.load('C:/Users/zhj20/PycharmProjects/alltest1/game_make/sound/background.ogg')  # 这个会重复播放，且唯一？
pg.mixer.music.set_volume(0.3)
# 死亡音乐
die_sound = pg.mixer.Sound('C:/Users/zhj20/PycharmProjects/alltest1/game_make/sound/rumble.ogg')
# 吃到奖励
gun_sound = pg.mixer.Sound('C:/Users/zhj20/PycharmProjects/alltest1/game_make/sound/pow0.wav')
shield_sound = pg.mixer.Sound('C:/Users/zhj20/PycharmProjects/alltest1/game_make/sound/pow1.wav')


def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    '''
    render(self,text: Union[str, bytes, None],antialias: bool | Literal[0] | Literal[1],color: ColorValue,
        background: Optional[ColorValue] = None,) 
    '''
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)


# print(rock_imgs)


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)  # 黑色变透明
        self.rect = self.image.get_rect()  # 外面的框
        self.radius = 20
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0

    def update(self):
        now = pg.time.get_ticks()
        # print(now - self.gun_time)
        if now - self.gun_time > 5000:
            self.gun = 1

        if self.hidden and pg.time.get_ticks() - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.y = HEIGHT - self.rect.height - 10

        key_pressed = pg.key.get_pressed()
        if key_pressed[pg.K_RIGHT]:
            self.rect.x += self.speed
        if key_pressed[pg.K_LEFT]:
            self.rect.x -= self.speed
        if key_pressed[pg.K_UP]:
            self.rect.y -= self.speed
        if key_pressed[pg.K_DOWN]:
            self.rect.y += self.speed
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        if not self.hidden:
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                pg.mixer.Sound.play(shoot_sound)
            elif self.gun >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.top)
                bullet2 = Bullet(self.rect.right, self.rect.top)
                all_sprites.add(bullet1, bullet2)
                bullets.add(bullet1, bullet2)
                pg.mixer.Sound.play(shoot_sound)

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
        self.image_ori = random.choice(rock_imgs)
        self.image = pg.Surface((50, 50))
        self.image = self.image_ori.copy()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()  # 外面的框
        # pg.draw.rect(self.image, RED, self.rect)
        self.radius = self.rect.width * 0.85 / 2
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -110)
        self.speedy = random.randrange(1, 3)
        self.speedx = random.randrange(-3, 3)
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
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 3)
            self.speedx = random.randrange(-3, 3)


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((20, 20))
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()  # 外面的框
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -5

    def update(self):
        self.rect.y += self.speedy
        key_pressed = pg.key.get_pressed()
        if self.rect.bottom < 0:
            self.kill()


class Exploration(pg.sprite.Sprite):
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
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
            if self.frame == len(expl_anim[self.size]):  # 如果是最后一张图片的话
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                # 重新定位;如果不这样做，可能会导致精灵在动画过程中移动或是抖动，就如陨石旋转那部分一样
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center


class Death(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.image = player_expl_img[0]
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
            if self.frame == len(player_expl_img):  # 如果是最后一张图片的话
                self.kill()
            else:
                self.image = player_expl_img[self.frame]
                # 重新定位;如果不这样做，可能会导致精灵在动画过程中移动或是抖动，就如陨石旋转那部分一样
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center


class Power(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()  # 外面的框
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y >= HEIGHT:
            self.kill()


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

pg.mixer.music.play(-1)


def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)


def draw_health(surf, hp, x, y, text, size):
    if hp <= 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = hp / 100 * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, RED, fill_rect)  # 血条
    pg.draw.rect(surf, WHITE, outline_rect, 2)  # 血条外框
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
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
    draw_text(screen, '打飞机', 64, WIDTH / 2, HEIGHT / 4 - 100)
    draw_text(screen, '↑↓←→移动飞船，space发射子弹', 20, WIDTH / 2, HEIGHT / 4 + 100)
    draw_text(screen, '任意键开始游戏', 18, WIDTH / 2, HEIGHT / 4 + 300)
    pg.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)  # 一秒跑十次
        # 取得输入
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return True
            elif event.type == pg.KEYUP:
                waiting = False
                return False


# 游戏循环
running = True
show_init = True
while running:
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
    clock.tick(FPS)  # 一秒跑十次
    # 取得输入
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.shoot()

    # 更新
    all_sprites.update()
    # 子弹和陨石
    hits = pg.sprite.groupcollide(rocks, bullets, True, True)  # 后面两个参数是判断碰撞后要不要删除;返回值是字典；默认矩形碰撞判断
    for hit in hits:
        pg.mixer.Sound.play(random.choice(expl_sounds))
        score += int(hit.radius)
        expl = Exploration(hit.rect.center, 'big')
        all_sprites.add(expl)
        if random.random() > 0.1:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            # powers = pg.sprite.Group() 这个地方加上去就在发射时吃不到道具了，因为创建了一个新的精灵模组，飞机只能和最后的发生互动
            powers.add(pow)
        new_rock()
    # 飞机和陨石
    hits = pg.sprite.spritecollide(player, rocks, True, pg.sprite.collide_circle)  # 需要在类中加radius
    # if hits:
    #     player.health -= 10
    #     r = Rock()
    #     all_sprites.add(r)
    #     rocks.add(r)
    # 根据大小扣血
    for hit in hits:
        expl = Exploration(hit.rect.center, 'small')
        all_sprites.add(expl)
        player.health -= int(hit.radius)
        # print(player.health)
        new_rock()
        if player.health <= 0:
            death = Death(player.rect.center)
            pg.mixer.Sound.play(die_sound)
            all_sprites.add(death)
            player.health = 100
            player.lives -= 1
            # print(player.lives)
            player.hide()
    if player.lives < 0 and not (death.alive()):
        # print('you lost')
        show_init = True
    '''
    death这个变量是在第一个if语句中定义的，所以它属于局部作用域。
    但是，Python会在嵌套作用域中查找变量，如果在局部作用域找不到，就会去上一层作用域查找。
    所以，在第二个if语句中，可以使用death这个变量，因为它是在上一层作用域中定义的。
    '''
    # 飞机和宝物
    hits = pg.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'shield':
            pg.mixer.Sound.play(shield_sound)
            player.health += 10
            if player.health >= 100:
                player.health = 100
        if hit.type == 'gun':
            pg.mixer.Sound.play(gun_sound)
            player.gunup()

    # 画面显示；颜色传入元组
    screen.blit(background_img, (0, 0))  # 显示图片的方法
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_health(screen, player.health, 10, 10, str(player.health), 18)
    draw_lives(screen, player.lives, player_lives_img, HEIGHT - 190, 15)

    # 更新画面
    pg.display.update()

# 退出
pg.quit()
