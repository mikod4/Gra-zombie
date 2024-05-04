import pygame
from config import cfg
import Player
import Projectile
import Zombie_Killed_Particles
import Enemy_Normal
import Enemy_Boss
import Enemy_Big
import Enemy_Charger
from random import randint
from random import choice
from time import sleep
from datetime import datetime

# read config data and assign:
# screen properties
X = cfg['Screen_x']
Y = cfg['Screen_y']
screen_color = cfg['screen_color']
fps = cfg['fps']

# font properties
font_name = cfg['font_name']
font_size = cfg['font_size']

# player properties
player_x = X // 2
player_y = Y // 2
player_speed = cfg['player_speed']

# player stats levels:
speed_level = 0
shoot_cooldown_level = 0
damage_level = 0
range_level = 0
# score
score = 0
level = 1

# enemies properties
enemy_number = cfg['enemy_number']
enemy_list = [Enemy_Normal]
enemies_killed = 0


# get max score from file
def get_max_score():
    """Function is reading max score from file and returns it"""
    file = open('max_score.txt', 'r')
    line = file.read()
    file.close()
    return int(line)


# update max score in file
def update_max_score(top):
    """Functions checks if current score is higher and if so it writes it to file"""
    if top > max_score:
        file = open('max_score.txt', 'w')
        file.write(str(top))
        file.close()


# start properties
def start():
    """functions initialises screen and sets name of the window"""
    # start screen
    screen.fill(screen_color)
    pygame.display.set_caption("Zombie")
    pygame.display.flip()


# start screen text
def start_screen(font_name):
    """Functions is responsible for starting game and waiting for start input"""
    font = pygame.font.Font(font_name, 2 * font_size)
    text = font.render("Press any key to start", True, (0, 0, 0), screen_color)
    text_rect = text.get_rect()
    text_rect.center = (X // 2, Y // 2)
    screen.blit(text, text_rect)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                global running
                running = True
                return


# game over text
def game_over_screen(font_name):
    """Functions displays game over screen and waits for input if player wants to start again
    or end the game"""
    global level
    global running
    font = pygame.font.Font(font_name, 2 * font_size)
    text = font.render(
        "Game Over Press any key to start again", True, (0, 0, 0), screen_color
    )
    text_rect = text.get_rect()
    text_rect.center = (X // 2, Y // 2)
    screen.blit(text, text_rect)
    pygame.display.flip()
    update_max_score(level)
    sleep(1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # if escape exit game
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                # Reset all values
                global player
                global projectile_list
                global enemies
                global score
                global enemy_number
                global enemy_list

                # Initialize player
                player = Player.Player(player_x, player_y)

                # Initialize Projectile
                projectile_list = list()

                # Initialize Enemy
                enemies = list()

                score = 0
                level = 1
                enemy_number = 1
                enemy_list = [Enemy_Normal]

                # reset stats
                global speed_level
                global damage_level
                global range_level

                speed_level = 0
                damage_level = 0
                range_level = 0

                return


# display player score
def write_score(score):
    """Function is writing player score (balance)"""
    font = pygame.font.Font(font_name, 2 * font_size)
    text = font.render("Balance: $" + str(score), True, (0, 200, 0), screen_color)
    text_rect = text.get_rect()
    text_rect.right = X - 5
    screen.blit(text, text_rect)


remaining_cooldown = datetime.now().minute * 3600 + datetime.now().second * 60 + datetime.now().microsecond // 100000


def shoot_cooldown():
    """Function checks if shot is still on cooldown, if not it sets new cooldown. Returns True or False
    depending if shot is on cooldown or not."""
    global remaining_cooldown
    current_time = datetime.now().minute * 3600 + datetime.now().second * 60 + datetime.now().microsecond // 100000
    if remaining_cooldown - current_time <= 0:
        remaining_cooldown = current_time + cfg[
            'player_shooting_cooldown'] - shoot_cooldown_level
        return True
    return False


# player shooting function
def player_shoot_hold():
    """Function allows player to hold arrow to shoot. It appends new bullets to projectiles list"""
    # player shoot controls
    key = pygame.key.get_pressed()
    if key[pygame.K_UP] and shoot_cooldown():
        projectile_list.append(
            Projectile.Projectile(
                player.x + player.player_size // 2,
                player.y + player.player_size // 2,
                "up",
            )
        )
    elif key[pygame.K_DOWN] and shoot_cooldown():
        projectile_list.append(
            Projectile.Projectile(
                player.x + player.player_size // 2,
                player.y + player.player_size // 2,
                "down",
            )
        )
    elif key[pygame.K_LEFT] and shoot_cooldown():
        projectile_list.append(
            Projectile.Projectile(
                player.x + player.player_size // 2,
                player.y + player.player_size // 2,
                "left",
            )
        )
    elif key[pygame.K_RIGHT] and shoot_cooldown():
        projectile_list.append(
            Projectile.Projectile(
                player.x + player.player_size // 2,
                player.y + player.player_size // 2,
                "right",
            )
        )


pressed = False


def player_shoot_press(event):
    """Function allow player to shoot on button press, not hold. If player presses button it
    adds new bullet to projectile list."""
    global pressed

    pressed = True

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            projectile_list.append(
                Projectile.Projectile(
                    player.x + player.player_size // 2,
                    player.y + player.player_size // 2,
                    "up",
                )
            )
        elif event.key == pygame.K_DOWN:
            projectile_list.append(
                Projectile.Projectile(
                    player.x + player.player_size // 2,
                    player.y + player.player_size // 2,
                    "down",
                )
            )
        elif event.key == pygame.K_LEFT:
            projectile_list.append(
                Projectile.Projectile(
                    player.x + player.player_size // 2,
                    player.y + player.player_size // 2,
                    "left",
                )
            )
        elif event.key == pygame.K_RIGHT:
            projectile_list.append(
                Projectile.Projectile(
                    player.x + player.player_size // 2,
                    player.y + player.player_size // 2,
                    "right",
                )
            )


# check if player went over the screen edge
def check_if_player_in_map(x, y):
    """Function checks if player on his next move is going to be on map, if not it returns false, which
    means player is not allowed to move in that direction, true if he is."""
    if x > X - player.player_size or x < 0 or y > Y - player.player_size or y < 0:
        return False

    return True


# player movement function
def player_move():
    """Function is handling player movement. It changes variable x and y in Player object depending
    on keyboard input."""
    key = pygame.key.get_pressed()

    # player move controls
    if key[pygame.K_w]:
        if check_if_player_in_map(player.x, player.y - player_speed):
            player.player_move(player.x, player.y - player_speed)
    if key[pygame.K_s]:
        if check_if_player_in_map(player.x, player.y + player_speed):
            player.player_move(player.x, player.y + player_speed)
    if key[pygame.K_a]:
        if check_if_player_in_map(player.x - player_speed, player.y):
            player.player_move(player.x - player_speed, player.y)
    if key[pygame.K_d]:
        if check_if_player_in_map(player.x + player_speed, player.y):
            player.player_move(player.x + player_speed, player.y)


# boss spawning function
def spawn_boss():
    """Function spawns boss on map at random edge of the map."""
    global enemies
    random_x = choice([0, X])
    if random_x == 0:
        random_y = randint(0, Y)
    else:
        random_x = randint(0, X)
        random_y = 0

    enemies.append(Enemy_Boss.Enemy(random_x, random_y, level))


# add new zombie types
def new_enemy(level):
    """Function depending on game level is adding new enemies to list of available enemies
    for current level."""
    # needs fix
    global enemy_list
    if level % 10 == 0:
        spawn_boss()
    match level:
        case 2:
            enemy_list.append(Enemy_Big)
        case 5:
            enemy_list.append(Enemy_Charger)


# increase number of zombies
def increase_enemy_number():
    """Function is consistently increasing number of enemies on map depending on game level."""
    global enemy_number
    global level
    if enemies_killed % (level * 10) == 0:
        enemy_number += 1
        level += 1
        # call new zombies
        new_enemy(level)


# generate new zombie
def generate_enemy():
    """Functions creates new Enemy object choosing randomly from available enemy list and chooses
    random edge of map to spawn it."""
    # generate enemies
    global enemies
    global enemy_list
    while len(enemies) < enemy_number:
        enemy_type = choice(enemy_list)
        random_x = choice([0, X])
        if random_x == 0:
            random_y = randint(0, Y)
        else:
            random_x = randint(0, X)
            random_y = 0

        enemies.append(enemy_type.Enemy(random_x, random_y))


# look for zombie and projectile collision
def check_projectile_collision(enemy):
    """Function checks if there is projectile and enemy collision. If so it changes enemy health
    according to bullet damage. It also increases score and removes dead enemies."""
    global enemies_killed
    global projectile_list
    global enemies
    global score

    for projectile in projectile_list:
        if pygame.Rect.colliderect(
                enemy.enemy_rect, projectile.projectile_rect
        ):
            projectile_list.remove(projectile)
            if not enemy.remove_health(projectile.damage + damage_level * cfg['projectile_upgrade_damage_amount']):
                # create random number of particles on enemy kill
                for _ in range(randint(cfg['min_particle_count'], cfg['max_particle_count'])):
                    particles.append(Zombie_Killed_Particles.Particle(enemy.name, enemy.x, enemy.y))
                enemies.remove(enemy)
                enemies_killed += 1
                score += enemy.value

                # check for increased enemies:
                increase_enemy_number()
                break


# display player stats
def draw_stats():
    """Function is drawing player stats."""
    global damage_level
    global speed_level
    global range_level
    global shoot_cooldown_level

    font = pygame.font.Font(font_name, font_size)

    left = 0
    top = font_size + 5

    bullet_damage = cfg['projectile_damage']
    bullet_damage_text = font.render(
        "Damage: " + str(bullet_damage + damage_level * cfg['projectile_upgrade_damage_amount']), True, (0, 0, 0),
        screen_color)
    bullet_damage_text_rect = bullet_damage_text.get_rect()
    bullet_damage_text_rect.left = left
    bullet_damage_text_rect.top = 0 * top

    bullet_range = cfg['projectile_range']
    bullet_range_text = font.render(
        "Range: " + str(bullet_range + range_level * cfg['projectile_upgrade_range_amount']), True, (0, 0, 0),
        screen_color)
    bullet_range_text_rect = bullet_range_text.get_rect()
    bullet_range_text_rect.left = left
    bullet_range_text_rect.top = 1 * top

    player_speed = cfg['player_speed']
    player_speed_text = font.render("Speed: " + str(player_speed + speed_level * cfg['player_speed_upgrade_amount']),
                                    True, (0, 0, 0), screen_color)
    player_speed_text_rect = player_speed_text.get_rect()
    player_speed_text_rect.left = left
    player_speed_text_rect.top = 2 * top

    cooldown = cfg['player_shooting_cooldown']
    cd = str(cooldown - shoot_cooldown_level)
    if cooldown - shoot_cooldown_level == 1:
        cd = "Max Level"
    cooldown_text = font.render("Cooldown: " + cd, True, (0, 0, 0), screen_color)
    cooldown_text_rect = cooldown_text.get_rect()
    cooldown_text_rect.left = left
    cooldown_text_rect.top = 3 * top

    screen.blit(bullet_damage_text, bullet_damage_text_rect)
    screen.blit(bullet_range_text, bullet_range_text_rect)
    screen.blit(player_speed_text, player_speed_text_rect)
    screen.blit(cooldown_text, cooldown_text_rect)


# display current and highest level
def draw_level():
    """Function is drawing current and highest level."""
    global level
    global max_score

    font = pygame.font.Font(font_name, font_size)

    level_text = font.render(f"Level: {level}", True, (0, 0, 0), screen_color)
    level_text_rect = level_text.get_rect()
    level_text_rect.center = (X // 2, 0 + font_size)

    max_score_text = font.render(f"Best: {max_score}", True, (0, 0, 0), screen_color)
    max_score_text_rect = level_text.get_rect()
    max_score_text_rect.center = (X // 2, font_size + font_size + 5)

    screen.blit(level_text, level_text_rect)
    screen.blit(max_score_text, max_score_text_rect)


# display shop information
def draw_shop():
    """Function draws shop information and prices on bottom of screen."""
    font = pygame.font.Font(font_name, font_size)
    upgrade_text = f"Upgrades shop: [1] Damage: ${cfg['projectile_upgrade_damage_cost']}  [2] Range: $40  [3] Speed: ${cfg['player_speed_upgrade_cost']}  [4] Cooldown: ${cfg['player_shooting_cooldown_cost']}"
    header_text = font.render(upgrade_text, True, (0, 0, 0), screen_color)
    header_text_rect = header_text.get_rect()
    header_text_rect.center = (X // 2, Y - font_size)

    screen.blit(header_text, header_text_rect)


# shopping event handler
def shop(event):
    """Shop handles buying upgrades form shop. It updates player balance if sth was bought."""
    global score
    global damage_level
    global speed_level
    global range_level
    global shoot_cooldown_level
    if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
        if score >= cfg['projectile_upgrade_damage_cost']:
            score -= cfg['projectile_upgrade_damage_cost']
            damage_level += 1
    if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
        if score >= cfg['projectile_upgrade_range_cost']:
            score -= cfg['projectile_upgrade_range_cost']
            range_level += 1
    if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
        if score >= cfg['player_speed_upgrade_cost']:
            score -= cfg['player_speed_upgrade_cost']
            speed_level += 1
            global player_speed
            player_speed += cfg['player_speed_upgrade_amount']
    if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
        if shoot_cooldown_level != 4:
            if score >= cfg['player_shooting_cooldown_cost']:
                score -= cfg['player_shooting_cooldown_cost']
                shoot_cooldown_level += 1


# max score
max_score = get_max_score()

# game start
pygame.init()
screen = pygame.display.set_mode((X, Y))
clock = pygame.time.Clock()
running = False
start()
start_screen(font_name)

# Initialize player
player = Player.Player(player_x, player_y)

# Initialize Projectile
projectile_list = list()

# List of enemies
enemies = list()

# List of particles
particles = list()


# main loop
def main():
    global running
    global score
    global pressed

    while running:
        # Draw screen
        screen.fill(screen_color)

        # Draw score
        write_score(score)

        # Draw stats
        draw_stats()

        # Draw level
        draw_level()

        # Draw shop info
        draw_shop()

        # Quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                running = False

            # listen for player shopping
            shop(event)

            # listen for shooting
            player_shoot_press(event)

        # player move
        player_move()

        # player shoot
        if not pressed:
            player_shoot_hold()
        pressed = False

        # Draw player
        pygame.draw.rect(screen, cfg['player_color'], player.player_rect)

        # Draw projectiles
        for projectile in projectile_list:
            # remove projectile if not on map
            if ((projectile.y > Y or projectile.y < 0) or (projectile.x > X or projectile.x < 0) or
                    (projectile.x > (projectile.start_x + projectile.range + range_level * cfg[
                        'projectile_upgrade_range_amount']) or projectile.x < (
                             projectile.start_x - projectile.range - range_level * cfg[
                         'projectile_upgrade_range_amount'])) or
                    (projectile.y > (projectile.start_y + projectile.range + range_level * cfg[
                        'projectile_upgrade_range_amount']) or projectile.y < (
                             projectile.start_y - projectile.range - range_level * cfg[
                         'projectile_upgrade_range_amount']))):
                projectile_list.remove(projectile)

            pygame.draw.rect(screen, (0, 0, 0), projectile.projectile_rect)
            projectile.travel()

        # Generate enemies
        generate_enemy()

        # Draw enemies and check for collision
        for enemy in enemies:
            # collision
            check_projectile_collision(enemy)

            # game over screen
            if pygame.Rect.colliderect(enemy.enemy_rect, player.player_rect):
                game_over_screen(font_name)

            # enemy movement
            enemy.move_to_player(player.x, player.y)

            # enemy draw
            pygame.draw.rect(screen, enemy.enemy_color, enemy.enemy_rect)

            # enemy health
            screen.blit(enemy.health_text, enemy.enemy_rect)

        # Draw particles
        for particle in particles:
            particle.x += choice([-particle.velocity_x, particle.velocity_x])
            particle.y += choice([-particle.velocity_y, particle.velocity_y])
            particle.duration -= 0.1
            pygame.draw.circle(screen, particle.color, (particle.x, particle.y), particle.duration)
            if particle.duration <= 0:
                particles.remove(particle)
        # refresh screen
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


main()
