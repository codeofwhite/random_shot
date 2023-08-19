import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 600
window_height = 800
game_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Wings of Dragon Slayer")

pygame.mixer.music.load(
    'C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/background_music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

start_game = False

# Define game colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (0, 255, 255)

# Define player properties
player_width = 70
player_height = 70
player_x = window_width / 2 - player_width / 2
player_y = window_height - player_height - 10
player_speed = 5
player_lives = 5
player_invisible = False
player_invisible_delay_time = 120
player_flash_delay = 20
player_can_shoot = True
player_shoot_delay = 20
player_bullets_speed = 0
bomb_count = 0
spread_bullet = False

# Define bullet properties
bullet_width = 20
bullet_height = 35
bullet_speed = 10

# Define enemy properties
enemy_width = 70
enemy_height = 70
enemy_speed = 3
enemy_spawn_delay = 60
enemy_bullet_speed = 5
enemy_fire_delay = 60

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

# Define item properties
item_width = 30
item_height = 30
item_speed = 3
item_spawn_delay = 60
item_types = ['bullet_speed_up']

# Create player sprite
player_sprite = pygame.Rect(player_x, player_y, player_width, player_height)

# Create boss sprite
boss_sprite = pygame.Rect(200, 100, 300, 120)

# Create lists for bullets and enemies
player_bullets = []
enemies = []
enemy_bullets = []
boss_lasers = []
items = []

# Set up game clock
clock = pygame.time.Clock()


# 道具
def create_item():
    # Create a new item sprite
    item_type = random.choice(item_types)
    item_x = random.randint(0, window_width - item_width)
    item_y = 0 - item_height
    item_sprite = pygame.Rect(item_x, item_y, item_width, item_height)
    if random.random() < 0.1:
        items.append((item_sprite, "bullet_speed_up"))
    elif random.random() < 0.1:
        items.append((item_sprite, "bomb"))
    # return item_sprite, item_type


# Define functions for creating and updating game objects
# 创造敌人
def create_enemy():
    # Create a new enemy sprite
    enemy_x = random.randint(0, window_width - enemy_width)
    enemy_y = 0 - enemy_height
    enemy_sprite = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    enemies.append(enemy_sprite)
    # print("Enemy spawned, total enemies: ", len(enemies))


# 敌人的子弹
def create_enemy_bullet(enemy):
    # Create a new enemy bullet sprite
    bullet_x = enemy.centerx - bullet_width / 2
    bullet_y = enemy.bottom
    bullet_sprite = pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
    enemy_bullets.append(bullet_sprite)


# 更新敌人
def update_player():
    global player_invisible, player_invisible_delay, player_invisible_delay_time
    global player_can_shoot, player_shoot_delay
    # Move the player based on user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_sprite.left > 0:
        player_sprite.move_ip(-player_speed, 0)
    if keys[pygame.K_RIGHT] and player_sprite.right < window_width:
        player_sprite.move_ip(player_speed, 0)
    if keys[pygame.K_UP] and player_sprite.top > 0:
        player_sprite.move_ip(0, -player_speed)
    if keys[pygame.K_DOWN] and player_sprite.bottom < window_height:
        player_sprite.move_ip(0, player_speed)
    if player_can_shoot:
        create_player_bullet()
        player_can_shoot = False  # disable shooting temporarily
        player_shoot_delay = 20 - player_bullets_speed  # set delay based on current level
        if player_shoot_delay <= 0:
            player_shoot_delay = 1
    # Decrement the shoot delay timer
    if not player_can_shoot:
        player_shoot_delay -= 1
        if player_shoot_delay == 0:
            player_can_shoot = True

    # Make the player briefly invisible if they have just lost a life
    if player_invisible:
        player_invisible_delay -= 1
        if player_invisible_delay == 0:
            player_invisible = False
            # player_sprite.bottom = window_height - 10


# 玩家子弹
def create_player_bullet():
    # Create a new player bullet sprite
    global spread_bullet
    bullet_x = player_sprite.centerx - bullet_width / 2
    bullet_y = player_sprite.top - bullet_height
    bullet_sprite = pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
    player_bullets.append((bullet_sprite, "front"))

    if spread_bullet == True:
        bullet_sprite_left = pygame.Rect(bullet_x - 10, bullet_y, bullet_width, bullet_height)
        bullet_sprite_right = pygame.Rect(bullet_x + 10, bullet_y, bullet_width, bullet_height)
        player_bullets.append((bullet_sprite_left, "left"))
        player_bullets.append((bullet_sprite_right, "right"))


# 玩家子弹的更新
def update_player_bullets():
    # create_player_bullet()
    # Move and remove player bullets that have gone offscreen
    for bullet in player_bullets:
        if bullet[1] == "front":
            bullet[0].move_ip(0, -bullet_speed)
            if bullet[0].bottom < 0:
                player_bullets.remove(bullet)
        elif bullet[1] == "left":
            bullet[0].move_ip(bullet_speed / 4, -bullet_speed)
            if bullet[0].bottom < 0:
                player_bullets.remove(bullet)
        elif bullet[1] == "right":
            bullet[0].move_ip(-bullet_speed / 4, -bullet_speed)
            if bullet[0].bottom < 0:
                player_bullets.remove(bullet)


# 对很多敌人进行更新
def update_enemies():
    # Move and remove enemies that have gone offscreen
    global player_invisible, player_invisible_delay, player_lives, game_over, player_invisible_delay_time
    for enemy in enemies:
        enemy.move_ip(0, enemy_speed)
        if enemy.top > window_height:
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
        if enemy_fire_delay == 0 and not enemy.colliderect(player_sprite):
            create_enemy_bullet(enemy)
            enemy_fire_delay = 60
        if not player_invisible:
            if player_sprite.colliderect(enemy):
                player_lives -= 1
                enemies.remove(enemy)
                if player_lives == 0:
                    game_over = True
                else:
                    # Make the player briefly invisible if they have just lost a life

                    player_invisible = True
                    player_invisible_delay = player_invisible_delay_time
                # player_sprite.bottom = -100


# 敌人子弹的更新
def update_enemy_bullets():
    # Move and remove enemy bullets that have gone offscreen
    for bullet in enemy_bullets:
        bullet.move_ip(0, enemy_bullet_speed)
        if bullet.top > window_height:
            enemy_bullets.remove(bullet)


# 子弹打击的效果
def check_collisions():
    # Check for collisions between player bullets and enemies
    global score
    for bullet in player_bullets:
        for enemy in enemies:
            if bullet[0].colliderect(enemy):
                player_bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                if random.random() < 0.1:
                    item_x = enemy.centerx - item_width / 2
                    item_y = enemy.bottom
                    item_sprite = pygame.Rect(item_x, item_y, item_width, item_height)
                    items.append((item_sprite, "bullet_speed_up"))
                # Add chance for enemy to drop bomb item
                elif random.random() < 0.1:
                    item_x = enemy.centerx - item_width / 2
                    item_y = enemy.bottom
                    item_sprite = pygame.Rect(item_x, item_y, item_width, item_height)
                    items.append((item_sprite, "bomb"))

            # Check for collisions between player and enemy bullets
    global player_lives, game_over
    global player_invisible, player_invisible_delay, player_invisible_delay_time
    if not player_invisible:
        for bullet in enemy_bullets:
            if bullet.colliderect(player_sprite):
                enemy_bullets.remove(bullet)
                player_lives -= 1
                if player_lives == 0:
                    game_over = True
                else:
                    # Make the player briefly invisible if they have just lost a life
                    player_invisible = True
                    player_invisible_delay = player_invisible_delay_time
                    # player_sprite.bottom = -100


# 等级
def create_level():
    global level, enemy_speed, enemy_fire_delay, enemy_spawn_delay, enemies_spawned, enemies_to_spawn, enemy_bullet_speed
    level += 1
    enemy_speed += 2
    enemy_fire_delay -= 10
    enemy_spawn_delay = 50
    enemies_spawned = 0
    enemies_to_spawn += 10
    enemy_bullet_speed += 2


# boss
def create_boss():
    global boss_sprite, boss_health, boss_attack_delay, boss_bullet_speed
    boss_sprite = pygame.Rect(200, 100, 300, 120)
    boss_health = 1000
    boss_attack_delay = 60
    boss_bullet_speed = 10


# boss的技能
def create_boss_laser():
    # Create a new laser sprite
    laser_width = 100
    laser_height = 150
    laser_x = boss_sprite.centerx - laser_width / 2
    laser_y = boss_sprite.bottom
    laser_sprite = pygame.Rect(laser_x, laser_y, laser_width, laser_height)
    boss_lasers.append(laser_sprite)


# boss的更新
def update_boss():
    global boss_sprite, boss_health, boss_attack_delay, boss_bullet_speed, game_over
    if boss_health > 0:
        # Move the boss around randomly
        boss_sprite.move_ip(random.randint(-10, 10), random.randint(-10, 10))
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
    if boss_attack_delay == 0:
        create_boss_bullet()
        boss_attack_delay = 30

    global boss_laser_delay, laser_speed
    boss_laser_delay -= 1
    if boss_laser_delay == 0:
        create_boss_laser()
        # print (boss_laser_delay)
        boss_laser_delay = 240

    global player_invisible, player_invisible_delay, player_invisible_delay_time
    if not player_invisible:
        if player_sprite.colliderect(boss_sprite):
            # Move the boss away from the player
            if boss_sprite.centerx < player_sprite.centerx:
                boss_sprite.move_ip(-10, 0)
            else:
                boss_sprite.move_ip(10, 0)
            if boss_sprite.centery < player_sprite.centery:
                boss_sprite.move_ip(0, -10)
            else:
                boss_sprite.move_ip(0, 10)
            global player_lives
            player_lives -= 1
            if player_lives == 0:
                game_over = True
            else:
                # Make the player briefly invisible if they have just lost a life

                player_invisible = True
                player_invisible_delay = player_invisible_delay_time
                # player_sprite.bottom = -100

    for laser in boss_lasers:
        laser.move_ip(0, laser_speed)
        if not player_invisible:
            if laser.colliderect(player_sprite):
                boss_laser_delay = 240
                player_lives -= 1
                if player_lives == 0:
                    game_over = True
                else:
                    # Make the player briefly invisible if they have just lost a life
                    player_invisible = True
                    player_invisible_delay = player_invisible_delay_time
        if laser.bottom < 0:
            boss_lasers.remove(laser)


# boss发射的普通子弹
def create_boss_bullet():
    # Create a new boss bullet sprite
    bullet_x = boss_sprite.centerx - bullet_width / 2
    bullet_y = boss_sprite.bottom
    bullet_sprite = pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
    enemy_bullets.append(bullet_sprite)


# boss被打的效果
def check_boss_collisions():
    # Check for collisions between player bullets and the boss
    global player_invisible, player_invisible_delay, player_invisible_delay_time
    global boss_health, score
    for bullet in player_bullets:
        if bullet[0].colliderect(boss_sprite):
            player_bullets.remove(bullet)
            boss_health -= 10
            score += 10
    # Check for collisions between player and boss bullets
    global player_lives, game_over
    if not player_invisible:
        for bullet in enemy_bullets:
            if bullet.colliderect(player_sprite):
                enemy_bullets.remove(bullet)
                player_lives -= 1
                if player_lives == 0:
                    game_over = True
                else:
                    # Make the player briefly invisible if they have just lost a life

                    player_invisible = True
                    player_invisible_delay = player_invisible_delay_time
                # player_sprite.bottom = -100


def update_items():
    global player_bullets_speed, spread_bullet
    # Move and remove items that have gone offscreen
    for item in items:
        item[0].move_ip(0, item_speed)
        if item[0].top > window_height:
            items.remove(item)
        # Check for collisions between player and items
        if player_sprite.colliderect(item[0]):
            items.remove(item)
            if item[1] == 'bullet_speed_up':
                player_bullets_speed += 2
                # print (player_shoot_delay)
                if player_bullets_speed >= 14:
                    player_bullets_speed = 14
                    spread_bullet = True
            if item[1] == 'bomb':
                global bomb_count
                bomb_count += 1


def update_game():
    global enemies_spawned, enemies_to_spawn, level, enemy_spawn_delay, background_speed
    update_player()
    update_player_bullets()

    # Spawn new enemies at random intervals
    # print (enemy_spawn_delay, enemies_spawned, enemies_to_spawn)
    enemy_spawn_delay -= 1
    if (enemy_spawn_delay == 0):
        create_enemy()
        if level == 2:
            enemy_spawn_delay = 50
        else:
            enemy_spawn_delay = 60
        enemies_spawned += 1

    update_items()
    update_enemies()
    update_enemy_bullets()
    check_collisions()

    # Check if it's time to create a new level
    if (level == 1) and (enemies_spawned > 50):
        create_level()

    if (level == 2) and (enemies_spawned > 50):
        create_boss()
        level += 1

    if level == 3:
        if random.random() < 0.008:
            create_item()
        update_boss()
        check_boss_collisions()
        if boss_health <= 0:
            global game_over
            game_over = True


def draw_game():
    global player_flash_delay
    # Draw the boss laser
    # game_window.fill(white)
    if not player_invisible or (player_invisible and player_flash_delay % 10 < 5):
        # if (player_invisible and player_flash_delay % 10 < 5):
        #     print ("Check")
        game_window.blit(player_image, player_sprite)

    # game_window.blit(player_image, player_sprite)
    for bullet in player_bullets:
        # pygame.draw.rect(game_window, red, bullet[0])
        game_window.blit(player_bullet_image, bullet[0])
    for enemy in enemies:
        game_window.blit(enemy_image, enemy)
    for bullet in enemy_bullets:
        # pygame.draw.rect(game_window, red, bullet)
        game_window.blit(enemy_bullet_image, bullet)
    for item in items:
        if item[1] == 'bullet_speed_up':
            game_window.blit(power_item_image, item[0])
        elif item[1] == "bomb":
            game_window.blit(bomb_image, item[0])
    for laser in boss_lasers:
        game_window.blit(laser_image, laser)

    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, white)
    lives_text = font.render("Lives: " + str(player_lives), True, white)
    level_text = font.render("Level: " + str(level), True, white)
    bomb_text = font.render("Bombs: " + str(bomb_count), True, white)
    game_window.blit(bomb_text, (window_width - 120, 50))
    game_window.blit(score_text, (10, 10))
    game_window.blit(lives_text, (window_width - 100, 10))
    game_window.blit(level_text, (window_width / 2 - 50, 10))

    if level == 3:
        boss_health_text = font.render("Boss Health: " + str(boss_health), True, white)
        game_window.blit(boss_health_text, (window_width / 2 - 70, 50))
        game_window.blit(boss_image, boss_sprite)
        # pygame.draw.rect(game_window, black, boss_sprite)

    if player_invisible:
        player_flash_delay -= 1
        if player_flash_delay == 0:
            player_flash_delay = 20

    pygame.display.update()


# bullet_image = pygame.image.load("bullet.png")
player_image = pygame.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/game_sprite/player.png")
power_item_image = pygame.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/game_sprite/power_item.png")
enemy_image = pygame.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/game_sprite/enemy.png")
bomb_image = pygame.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/game_sprite/bomb.png")
boss_image = pygame.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/game_sprite/boss.png")
enemy_bullet_image = pygame.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/game_sprite/enemy_bullet.png")
player_bullet_image = pygame.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/game_sprite/player_bullet.png")
laser_image = pygame.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/game_sprite/laser.png")
pygame.display.set_icon(player_image)


# background_image = pygame.image.load("./game_sprite/background.png")

def use_bomb():
    global enemies, enemy_bullets, boss_health, bomb_count, level
    # Remove all enemies and enemy bullets
    enemies.clear()
    enemy_bullets.clear()
    # Reduce the boss health by 1000
    if level == 3:
        boss_health -= 1000
        if boss_health <= 0:
            boss_health = 0
    # Decrement the bomb count
    bomb_count -= 1


background_image = pygame.image.load(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/game_make_project/chapter_2_img/game_sprite/background.png")
background_rect = background_image.get_rect()

background_surface = pygame.Surface((600, 3200))
for x in range(0, 600, background_image.get_width()):
    for y in range(0, 3200, background_image.get_height()):
        background_surface.blit(background_image, (x, y))

background_position = [0, -window_height]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if bomb_count > 0:
            use_bomb()

    if not game_over and start_game:

        background_position[1] += 1
        if background_position[1] > 0:
            background_position[1] -= 1600

        # Draw the background surface onto the game window
        game_window.blit(background_surface, background_position)

        update_game()
        draw_game()
        clock.tick(60)

    elif start_game == False:
        background_position[1] += 3
        if background_position[1] > 0:
            background_position[1] -= 1600

        # Draw the background surface onto the game window
        game_window.blit(background_surface, background_position)
        font = pygame.font.Font(None, 56)
        congrats_text = font.render(f"Wings of the Dragon Slayer", True, white)
        game_window.blit(congrats_text, (window_width / 2 - 250, window_height / 2 - 100))

        # Show restart instructions
        restart_text = font.render("Press Enter to start", True, white)
        game_window.blit(restart_text, (window_width / 2 - 175, window_height / 2))

        if keys[pygame.K_RETURN]:
            # Reset game variables
            score = 0
            player_lives = 5
            enemies_spawned = 0
            enemies_to_spawn = 20
            level = 1
            player_sprite.centerx = window_width / 2
            player_sprite.bottom = window_height - 10
            player_can_shoot = True
            player_shoot_delay = 5
            player_invisible = False
            player_flash_delay = 20
            player_bullets.clear()
            enemies.clear()
            enemy_bullets.clear()
            boss_lasers.clear()
            items.clear()
            enemy_speed = 3
            enemy_spawn_delay = 60
            enemy_bullet_speed = 5
            enemy_fire_delay = 60
            player_bullets_speed = 0
            item_spawn_delay = 60
            item_speed = 3
            boss_health = 1000
            spread_bullet = False
            start_game = True
            game_over = False
            bomb_count = 0
        clock.tick(60)
        pygame.display.update()

    elif (boss_health == 0) and game_over:
        # Move the background image down
        background_position[1] += 3
        if background_position[1] > 0:
            background_position[1] -= 1600

        # Draw the background surface onto the game window
        game_window.blit(background_surface, background_position)
        # game_window.fill(white)

        font = pygame.font.Font(None, 72)
        congrats_text = font.render(f"Congrats!", True, white)
        game_window.blit(congrats_text, (window_width / 2 - 200, window_height / 2 - 100))

        score_text = font.render(f"Your Score {score}", True, white)
        game_window.blit(score_text, (window_width / 2 - 200, window_height / 2 - 50))

        # Show restart instructions
        restart_text = font.render("Press R to restart", True, white)
        game_window.blit(restart_text, (window_width / 2 - 200, window_height / 2))

        # Check if R key is pressed to restart the game
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset game variables
            score = 0
            player_lives = 5
            enemies_spawned = 0
            enemies_to_spawn = 20
            level = 1
            player_sprite.centerx = window_width / 2
            player_sprite.bottom = window_height - 10
            player_can_shoot = True
            player_shoot_delay = 5
            player_invisible = False
            player_flash_delay = 20
            player_bullets.clear()
            enemies.clear()
            enemy_bullets.clear()
            boss_lasers.clear()
            items.clear()
            enemy_speed = 3
            enemy_spawn_delay = 60
            enemy_bullet_speed = 5
            enemy_fire_delay = 60
            player_bullets_speed = 0
            item_spawn_delay = 60
            item_speed = 3
            boss_health = 1000
            spread_bullet = False
            start_game = False
            bomb_count = 0
            # Create new level
            # create_level()
            game_over = False
        clock.tick(60)
        pygame.display.update()
    else:
        # Move the background image down
        background_position[1] += 3
        if background_position[1] > 0:
            background_position[1] -= 1600

        # Draw the background surface onto the game window
        game_window.blit(background_surface, background_position)
        # game_window.fill(white)

        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, white)
        game_window.blit(game_over_text, (window_width / 2 - 150, window_height / 2 - 100))

        score_text = font.render(f"Your Score {score}", True, white)
        game_window.blit(score_text, (window_width / 2 - 175, window_height / 2 - 50))

        # Show restart instructions
        restart_text = font.render("Press R to restart", True, white)
        game_window.blit(restart_text, (window_width / 2 - 200, window_height / 2))

        # Check if R key is pressed to restart the game
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset game variables
            score = 0
            player_lives = 5
            enemies_spawned = 0
            enemies_to_spawn = 20
            level = 1
            player_sprite.centerx = window_width / 2
            player_sprite.bottom = window_height - 10
            player_can_shoot = True
            player_shoot_delay = 5
            player_invisible = False
            player_flash_delay = 20
            player_bullets.clear()
            enemies.clear()
            enemy_bullets.clear()
            boss_lasers.clear()
            items.clear()
            enemy_speed = 3
            enemy_spawn_delay = 60
            enemy_bullet_speed = 5
            enemy_fire_delay = 60
            player_bullets_speed = 0
            item_spawn_delay = 60
            item_speed = 3
            boss_health = 1000
            spread_bullet = False
            start_game = False
            bomb_count = 0

            # Create new level
            # create_level()
            game_over = False
        clock.tick(60)
        pygame.display.update()

# pygame.quit()
