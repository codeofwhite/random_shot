import pygame
import random
import sys
import math
import mediapipe
import cv2

pygame.init()

# Set up the game window
window_width = 600
window_height = 780
game_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("chapter2")

# 图片
player_image = pygame.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/game_sprite/player.png")
power_item_image = pygame.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/game_sprite/power_item.png")
enemy_image = pygame.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/game_sprite/enemy.png")
bomb_image = pygame.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/game_sprite/bomb.png")
boss_image = pygame.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/imgs/boss.png")
boss_image = pygame.transform.scale(boss_image, (250, 250))
enemy_bullet_image = pygame.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/game_sprite/enemy_bullet.png")
player_bullet_image = pygame.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/game_sprite/player_bullet.png")
laser_image = pygame.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/game_sprite/laser.png")
pygame.display.set_icon(player_image)

# 音乐
pygame.mixer.music.load(
    'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/background_music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Define game colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (0, 255, 255)

# Set up game clock
clock = pygame.time.Clock()

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


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.speed = 5
        self.lives = 3
        self.health = 100
        self.player_invisible = False
        self.player_width = 70
        self.player_height = 70
        self.player_x = window_width / 2 - self.player_width / 2
        self.player_y = window_height - self.player_height - 10
        self.player_sprite = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)

    def update(self):
        if self.rect.right > window_width:
            self.rect.right = window_width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > window_height:
            self.rect.bottom = window_height
        if self.rect.top < 0:
            self.rect.top = 0


player = Player()

# Create boss sprite
boss_sprite = pygame.Rect(200, 100, 300, 120)

# 手势识别初始化
mp_drawing = mediapipe.solutions.drawing_utils  # mediapipe 繪圖方法
mp_drawing_styles = mediapipe.solutions.drawing_styles  # mediapipe 繪圖樣式
mp_hands = mediapipe.solutions.hands  # mediapipe 偵測手掌方法


def vector_2d_angle(v1, v2):
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_ = math.degrees(math.acos(
            (v1_x * v2_x + v1_y * v2_y) / (((v1_x ** 2 + v1_y ** 2) ** 0.5) * ((v2_x ** 2 + v2_y ** 2) ** 0.5))))
    except:
        angle_ = 180
    return angle_


# 手指的角度判断
def hand_angle(hand_):
    angle_list = []
    # thumb 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[2][0])), (int(hand_[0][1]) - int(hand_[2][1]))),
        ((int(hand_[3][0]) - int(hand_[4][0])), (int(hand_[3][1]) - int(hand_[4][1])))
    )
    '''
    解释：关节点：hand_的第一个空代表关节点，第二个空代表 x or y, 0对应x，1对应y
    把它们当成两个向量，计算其夹角
    '''
    angle_list.append(angle_)
    # index 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[6][0])), (int(hand_[0][1]) - int(hand_[6][1]))),
        ((int(hand_[7][0]) - int(hand_[8][0])), (int(hand_[7][1]) - int(hand_[8][1])))
    )
    angle_list.append(angle_)
    # middle 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[10][0])), (int(hand_[0][1]) - int(hand_[10][1]))),
        ((int(hand_[11][0]) - int(hand_[12][0])), (int(hand_[11][1]) - int(hand_[12][1])))
    )
    angle_list.append(angle_)
    # ring 無名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[14][0])), (int(hand_[0][1]) - int(hand_[14][1]))),
        ((int(hand_[15][0]) - int(hand_[16][0])), (int(hand_[15][1]) - int(hand_[16][1])))
    )
    angle_list.append(angle_)
    # pink 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[18][0])), (int(hand_[0][1]) - int(hand_[18][1]))),
        ((int(hand_[19][0]) - int(hand_[20][0])), (int(hand_[19][1]) - int(hand_[20][1])))
    )
    angle_list.append(angle_)
    return angle_list


# 根究不同手指的角度，返回对应的手势
def gesture(finger_angle):
    f1 = finger_angle[0]  # 大拇指角度
    f2 = finger_angle[1]  # 食指角度
    f3 = finger_angle[2]  # 中指角度
    f4 = finger_angle[3]  # 無名指角度
    f5 = finger_angle[4]  # 小拇指角度
    # 小於 50 表示手指伸直，大於等於 50 表示手指捲縮；全张开就趋于0度
    if f1 >= 50 and f2 >= 50 and f3 >= 50 and f4 >= 50 and f5 >= 50:
        return "rock"
    elif f1 >= 50 and f2 < 50 and f3 < 50 and f4 >= 50 and f5 >= 50:
        return "scissors"
    elif f1 < 50 and f2 < 50 and f3 < 50 and f4 < 50 and f5 < 50:
        return "paper"


def create_boss():
    global boss_sprite, boss_health, boss_attack_delay, boss_bullet_speed
    boss_sprite = pygame.Rect(200, 100, 300, 120)
    boss_health = 1000
    boss_attack_delay = 60
    boss_bullet_speed = 10


def update_boss():
    global boss_sprite, boss_health, boss_attack_delay, boss_bullet_speed, game_over
    if boss_health > 0:
        # Move the boss around randomly
        boss_sprite.move_ip(random.randint(-17, 17), random.randint(-17, 17))
        # Prevent the boss from going out of the game window
        if boss_sprite.left < 0:
            boss_sprite.left = 0
        if boss_sprite.right > window_width:
            boss_sprite.right = window_width
        if boss_sprite.top < 0:
            boss_sprite.top = 0
        if boss_sprite.bottom > window_height:
            boss_sprite.bottom = window_height
        # Fire bullets at the player
        boss_attack_delay -= 1
    # if boss_attack_delay == 0:
    #     create_boss_bullet()
    #     boss_attack_delay = 30

    # global boss_laser_delay, laser_speed
    # boss_laser_delay -= 1
    # if boss_laser_delay == 0:
    #     create_boss_laser()
    #     # print (boss_laser_delay)
    #     boss_laser_delay = 240

    if not player.player_invisible:
        if player.player_sprite.colliderect(boss_sprite):
            # Move the boss away from the player
            if boss_sprite.centerx <= player.rect.centerx:
                boss_sprite.move_ip(-10, 0)
            else:
                boss_sprite.move_ip(10, 0)
            if boss_sprite.centery <= player.rect.centery:
                boss_sprite.move_ip(0, -10)
            else:
                boss_sprite.move_ip(0, 10)


#         global player_lives
#         player_lives -= 1
#         if player_lives == 0:
#             game_over = True
#         else:
#             # Make the player briefly invisible if they have just lost a life
#
#             player_invisible = True
#             player_invisible_delay = player_invisible_delay_time
#             # player_sprite.bottom = -100

# for laser in boss_lasers:
#     laser.move_ip(0, laser_speed)
#     if not player_invisible:
#         if laser.colliderect(player_sprite):
#             boss_laser_delay = 240
#             player_lives -= 1
#             if player_lives == 0:
#                 game_over = True
#             else:
#                 # Make the player briefly invisible if they have just lost a life
#                 player_invisible = True
#                 player_invisible_delay = player_invisible_delay_time
#     if laser.bottom < 0:
#         boss_lasers.remove(laser)

flag = False


def update_game():
    global flag
    if flag:
        create_boss()
        flag = True
    update_boss()


def draw_game():
    font = pygame.font.Font(None, 36)
    boss_health_text = font.render("Boss Health: " + str(boss_health), True, white)
    game_window.blit(boss_health_text, (window_width / 2 - 70, 50))
    game_window.blit(boss_image, boss_sprite)


background_image = pygame.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/game_sprite/background_new.png")
background_rect = background_image.get_rect()

background_surface = pygame.Surface((600, 3200))
for x in range(0, 600, background_image.get_width()):
    for y in range(0, 3200, background_image.get_height()):
        background_surface.blit(background_image, (x, y))

background_position = [0, -window_height]

# 开启摄像头和显示的参数
cap = cv2.VideoCapture(0)  # 开启摄像头
fontFace = cv2.FONT_HERSHEY_SIMPLEX
lineType = cv2.LINE_AA


def game_start():
    with mp_hands.Hands(model_complexity=0, max_num_hands=1, min_detection_confidence=0.55, static_image_mode=False,
                        min_tracking_confidence=0.55) as hands:
        if not cap.isOpened():
            print("Cannot open camera")
            exit()

        running = True
        w, h = 600, 350  # 图像的尺寸
        cx, cy = 0, 0
        label = ''

        while True:
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
                        finger_angle = hand_angle(left_finger_points)
                        text = gesture(finger_angle)
                        cv2.putText(img, text, (30, 120), fontFace, 5, (255, 255, 255), 10, lineType)
                    for i in right_hand_landmarks.landmark:
                        x_ = i.x * w  # 这里乘w, h可以理解为线性变换
                        y_ = i.y * h
                        right_finger_points.append((x_, y_))
                    if right_finger_points:
                        finger_angle = hand_angle(right_finger_points)
                        text = gesture(finger_angle)
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

                # # 射击
                # if ggf.gesture(finger_angle) == 'rock' and label == 'Left':
                #     player.shoot_left()
                # if ggf.gesture(finger_angle) == 'rock' and label == 'Right':
                #     player.shoot_right()

            cv2.imshow('test', img)
            if cv2.waitKey(5) == ord('q'):
                break  # 按下 q 鍵停止
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cv2.destroyAllWindows()
                    return

            background_position[1] += 1
            if background_position[1] > 0:
                background_position[1] -= 1600

            # Draw the background surface onto the game window
            game_window.blit(background_surface, background_position)
            player.update()
            update_game()
            draw_game()
            game_window.blit(player_image, player)
            pygame.display.update()
            clock.tick(144)


if __name__ == '__main__':
    game_start()
