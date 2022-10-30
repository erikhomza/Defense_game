import pygame as pg
import random


pg.init()

clock = pg.time.Clock()
fps = 20
score = 0
shot_cooldown = 10
hp = 100
money = 0
spawn_cooldown = 3

screen_width = 1000
screen_height = 800

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
font = pg.font.Font("Turok.ttf", 40)
button_font = pg.font.Font("Turok.ttf", 30)

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Defense")

button_img = pg.image.load("cakeCenter.png").convert_alpha()
button_img = pg.transform.scale(button_img, (100, 50))
bg = pg.image.load("bg_castle.png").convert_alpha()
bg = pg.transform.scale(bg, (screen_width, screen_height))

screen.blit(bg, (0, 0))


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def pause(run, money, hp, weapon):
    button1 = Button(880, 700, button_img)
    button2 = Button(60, 700, button_img)
    button3 = Button(500, 700, button_img)
    button4 = Button(500, 500, button_img)
    button5 = Button(60, 500, button_img)
    button6 = Button(60, 300, button_img)
    game_paused = True
    make_defender = 0
    draw_text("SHOP", font, white, 500, 200)
    while game_paused:
        draw_text("BACK", button_font, black, 900, 705)
        draw_text("-130", font, black, 75, 300)
        draw_text("-100", font, black, 75, 500)
        draw_text("-30", font, black, 80, 700)
        draw_text("-100", font, black, 515, 500)
        draw_text("-30", font, black, 520, 700)
        draw_text("dual pistol", font, black, 55, 420)
        draw_text("+10 hp", font, black, 55, 620)
        draw_text("machine gun", font, black, 495, 420)
        draw_text("defender", font, black, 495, 620)
        draw_text("shotgun", font, black, 55, 220)
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_paused = False
                run = False
            if button1.draw(button1.rect.x, button1.rect.y):
                game_paused = False
            if button2.draw(button2.rect.x, button2.rect.y):
                if money >= 30:
                    money -= 30
                    hp += 10
            if button3.draw(button3.rect.x, button3.rect.y):
                if money >= 30:
                    money -= 30
                    make_defender += 1
            if button4.draw(button4.rect.x, button4.rect.y):
                if money >= 100 and weapon != 2:
                    money -= 100
                    weapon = 2
            if button5.draw(button5.rect.x, button5.rect.y):
                if money >= 100 and weapon != 3:
                    money -= 100
                    weapon = 3
            if button6.draw(button6.rect.x, button6.rect.y) and weapon != 4:
                if money >= 130:
                    money -= 130
                    weapon = 4
    return run, money, hp, make_defender, weapon


def reset_game():
    enemy_group.empty()
    enemy_bow_group.empty()
    bullet_group.empty()
    enemy_bullet_group.empty()
    defender_group.empty()
    player = Player(500, 500)
    hp = 100
    money = 0
    score = 0
    end = True
    while end:
        pg.display.update()
        draw_text("YOU LOST! press r to restart", font, white, (screen_width // 2) - 280, (screen_height // 2) - 80)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    end = False
    return hp, money, player, score


class Player:
    def __init__(self, x, y):
        self.weapon = 1
        img = pg.image.load("player1.png").convert_alpha()
        self.image = pg.transform.scale(img, (50, 50))
        self.img = pg.transform.scale(img, (50, 50))
        self.img.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = (0, -1)

    def update(self, x, y):
        key = pg.key.get_pressed()
        if self.weapon == 2:
            self.image = pg.image.load("player_w2.png").convert_alpha()
            self.img = pg.image.load("player_w2.png").convert_alpha()
        elif self.weapon == 3:
            self.image = pg.image.load("player_w3.png").convert_alpha()
            self.img = pg.image.load("player_w3.png").convert_alpha()
        elif self.weapon == 4:
            self.image = pg.image.load("player_w4.png").convert_alpha()
            self.img = pg.image.load("player_w4.png").convert_alpha()
        else:
            self.image = pg.image.load("player1.png").convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.can_shoot = True
        self.direction = (0, -1)
        if 0 < self.rect.y:
            if key[pg.K_UP]:
                self.rect.y -= 10
        if self.rect.y + 50 < screen_height:
            if key[pg.K_DOWN]:
                self.can_shoot = False
                self.image = pg.transform.rotate(self.img, 180)
                self.image.set_colorkey((255, 255, 255))
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.rect.y += 10
                self.direction = (0, 1)
        if 0 < self.rect.x:
            if key[pg.K_LEFT]:
                self.can_shoot = False
                self.image = pg.transform.rotate(self.img, 90)
                self.image.set_colorkey((255, 255, 255))
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.rect.x -= 10
                self.direction = (-1, 0)
        if self.rect.x + 50 < screen_width:
            if key[pg.K_RIGHT]:
                self.can_shoot = False
                self.image = pg.transform.rotate(self.img, 270)
                self.image.set_colorkey((255, 255, 255))
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.rect.x += 10
                self.direction = (1, 0)
        screen.blit(self.image, self.rect)


class Projectile(pg.sprite.Sprite):
    def __init__(self, x, y, direction, angle):
        super().__init__()
        img = pg.image.load("laserYellowVertical.png").convert_alpha()
        self.image = pg.transform.scale(img, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self. rect.y = y
        self.direction = direction
        self.angle = angle

    def update(self):
        if screen_height > self.rect.y > 0:
            self.rect.y += 20 * self.direction[1]
        else:
            self.kill()
        if screen_width > self.rect.x > 0:
            self.rect.x += 20 * self.direction[0]
        else:
            self.kill()
        screen.blit(pg.transform.rotate(self.image, self.angle), self.rect)


class Enemy(pg.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        number = random.randint(1, 4)
        img = pg.image.load(f"enemy{number}.png").convert_alpha()
        self.image = pg.transform.scale(img, (50, 50))
        self.image = pg.transform.flip(self.image, False, True)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0
        self.speed = random.randint(1, 4)
        self.attack_cooldown = 20

    def update(self, hp):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if pg.sprite.collide_rect(self, player):

            if self.attack_cooldown == 0:
                hp -= 1
                self.attack_cooldown = 20
        else:
            self.rect.y += self.speed
        screen.blit(self.image, self.rect)
        return hp


class EnemyBow(pg.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        number = random.randint(1, 4)
        img = pg.image.load(f"enemy-shooter{number}.png").convert_alpha()
        self.image = pg.transform.scale(img, (50, 50))
        self.image = pg.transform.flip(self.image, False, True)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0
        self.speed = random.randint(1, 2)
        self.shot_cooldown = 50

    def update(self):
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
        if self.rect.x - player.rect.x < 50 and player.rect.x - self.rect.x < 50 and player.rect.y > self.rect.y:
            pass
        else:
            self.rect.y += self.speed
        screen.blit(self.image, self.rect)


class EnemyProjectile(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pg.image.load("laserRedVertical.png").convert_alpha()
        self.image = pg.transform.scale(img, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.rect.y < screen_height:
            self.rect.y += 20
        else:
            self.kill()
        screen.blit(self.image, self.rect)


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self, x, y):
        action = False
        pos = pg.mouse.get_pos()

        if self.rect.collidepoint(pos):
            img = pg.image.load("grassCenter.png").convert_alpha()
            img = pg.transform.scale(img, (100, 50))
            self.rect = img.get_rect()
            self.rect.x = x
            self.rect.y = y
            screen.blit(img, self.rect)
            if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
        else:
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            screen.blit(self.image, self.rect)
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action


class Defender(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        number = random.randint(1, 4)
        img = pg.image.load(f"player{number}.png").convert_alpha()
        self.image = pg.transform.scale(img, (50, 50))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shot_cooldown = 60
        self.t = 0
        self.n = 0

    def update(self, x, y):
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1

        if self.t == 0:
            self.t = random.randint(2, 10)
            self.n = random.randint(-1, 1)
        else:
            if 0 < self.rect.x + 5 * self.n < 950:
                self.rect.x += 5 * self.n

            self.t -= 1

        screen.blit(self.image, self.rect)


player = Player(500, 500)
bullet_group = pg.sprite.Group()
enemy_bullet_group = pg.sprite.Group()
enemy_group = pg.sprite.Group()
enemy_bow_group = pg.sprite.Group()
button = Button(880, 700, button_img)
defender_group = pg.sprite.Group()

run = True
while run:

    if shot_cooldown > 0:
        shot_cooldown -= 1
    clock.tick(fps)
    screen.blit(bg, (0, 0))
    player.update(player.rect.x, player.rect.y)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    make_defender = 0

    spawn_cooldown -= 1
    if shot_cooldown == 0:
        spawn_cooldown = 5
        for i in range(20):
            n = random.randint(1, 700)
            if n == 25:
                enemy = Enemy(i * 50)
                enemy_group.add(enemy)
        for i in range(20):
            n = random.randint(1, 850)
            if n == 25:
                enemy_bow = EnemyBow(i * 50)
                enemy_bow_group.add(enemy_bow)
    for enemy in enemy_group:
        if pg.sprite.spritecollide(enemy, bullet_group, True):
            enemy.kill()
            money += 1
            score += 1
        if enemy.rect.y > 800:
            enemy.kill()
            hp -= 1
        pos = pg.mouse.get_pos()

    for bullet in enemy_bullet_group:
        if pg.sprite.spritecollide(player, enemy_bullet_group, True):
            hp -= 1

    for enemy_bow in enemy_bow_group:
        if pg.sprite.spritecollide(enemy_bow, bullet_group, True):
            enemy_bow.kill()
            money += 1
            score += 1
        if enemy_bow.rect.y > 800:
            enemy_bow.kill()
            hp -= 1

    for enemy_bow in enemy_bow_group:
        if enemy_bow.rect.x - player.rect.x < 50 and player.rect.x - enemy_bow.rect.x < 50 and player.rect.y > enemy_bow.rect.y:
            if enemy_bow.shot_cooldown == 0:
                enemy_bullet = EnemyProjectile(enemy_bow.rect.x + 25, enemy_bow.rect.y)
                enemy_bullet_group.add(enemy_bullet)
                enemy_bow.shot_cooldown = 50

    if button.draw(button.rect.x, button.rect.y):
        run, money, hp, make_defender, player.weapon = pause(run, money, hp, player.weapon)

    if make_defender > 0:
        for i in range(1, make_defender + 1):
            defender = Defender(random.randint(1, 15) * 50, random.randint(13, 15) * 50)
            defender_group.add(defender)

    key = pg.key.get_pressed()
    if shot_cooldown == 0:
        if key[pg.K_SPACE]:
            if player.weapon == 4:
                if player.direction == (0, -1):
                    bullet = Projectile(player.rect.x + 25, player.rect.y, (0.5, -0.5), 135)
                    bullet_group.add(bullet)
                    bullet = Projectile(player.rect.x + 25, player.rect.y, (0, -1), 0)
                    bullet_group.add(bullet)
                    bullet = Projectile(player.rect.x + 25, player.rect.y, (0.25, -0.75), 161)
                    bullet_group.add(bullet)
                    bullet = Projectile(player.rect.x + 25, player.rect.y, (-0.25, -0.75), 23)
                    bullet_group.add(bullet)
                    bullet = Projectile(player.rect.x + 25, player.rect.y, (-0.5, -0.5), 45)
                    bullet_group.add(bullet)
                elif player.direction == (0, 1):
                    bullet = Projectile(player.rect.x + 15, player.rect.y + 50, (0.5, 0.5), 180-135)
                    bullet_group.add(bullet)
                    bullet = Projectile(player.rect.x + 15, player.rect.y + 50, (0, 1), 0)
                    bullet_group.add(bullet)
                    bullet = Projectile(player.rect.x + 15, player.rect.y + 50, (0.25, 0.75), 180-161)
                    bullet_group.add(bullet)
                    bullet = Projectile(player.rect.x + 15, player.rect.y + 50, (-0.25, 0.75), 180-23)
                    bullet_group.add(bullet)
                    bullet = Projectile(player.rect.x + 15, player.rect.y + 50, (-0.5, 0.5), 180-45)
                    bullet_group.add(bullet)
                elif player.direction == (-1, 0):
                    bullet = Projectile(player.rect.x, player.rect.y + 15, (-0.5, 0.5), 90-135)
                    bullet_group.add(bullet)
                    bullet = Projectile(player.rect.x, player.rect.y + 15, (-1, 0), 90)
                    bullet_group.add(bullet)
                    bullet = Projectile(player.rect.x + 15, player.rect.y, (-0.75, 0.25), 90-161)
                    bullet_group.add(bullet)
                    bullet = Projectile(player.rect.x + 15, player.rect.y, (-0.75, -0.25), 90-23)
                    bullet_group.add(bullet)
                    bullet = Projectile(player.rect.x, player.rect.y + 15, (-0.5, -0.5), 90-45)
                    bullet_group.add(bullet)
                else:
                    bullet = Projectile(player.rect.x + 50, player.rect.y + 25, (0.5, 0.5), 270-45)
                    bullet_group.add(bullet)
                    bullet = Projectile(player.rect.x + 50, player.rect.y + 25, (1, 0), 270)
                    bullet_group.add(bullet)
                    bullet = Projectile(player.rect.x + 50, player.rect.y + 25, (0.75, 0.25), 270-23)
                    bullet_group.add(bullet)
                    bullet = Projectile(player.rect.x + 50, player.rect.y + 25, (0.75, -0.25), 270-161)
                    bullet_group.add(bullet)
                    bullet = Projectile(player.rect.x + 50, player.rect.y + 25, (0.5, -0.5), 270-135)
                    bullet_group.add(bullet)
                shot_cooldown = 40
            if player.weapon == 2 or player.weapon == 1:
                if player.direction == (0, -1):
                    bullet = Projectile(player.rect.x + 25, player.rect.y, player.direction, 0)
                elif player.direction == (0, 1):
                    bullet = Projectile(player.rect.x + 15, player.rect.y + 50, player.direction, 0)
                elif player.direction == (-1, 0):
                    bullet = Projectile(player.rect.x, player.rect.y + 15, player.direction, 90)
                else:
                    bullet = Projectile(player.rect.x + 50, player.rect.y + 25, player.direction, 270)
                bullet_group.add(bullet)
                if player.weapon == 2:
                    shot_cooldown = 5
                else:
                    shot_cooldown = 13
            if player.weapon == 3:
                if player.direction == (0, -1):
                    bullet = Projectile(player.rect.x, player.rect.y, player.direction, 0)
                elif player.direction == (0, 1):
                    bullet = Projectile(player.rect.x + 40, player.rect.y + 50, player.direction, 0)
                elif player.direction == (-1, 0):
                    bullet = Projectile(player.rect.x, player.rect.y, player.direction, 90)
                else:
                    bullet = Projectile(player.rect.x + 50, player.rect.y + 40, player.direction, 270)
                bullet_group.add(bullet)
                if player.direction == (0, -1):
                    bullet = Projectile(player.rect.x + 40, player.rect.y, player.direction, 0)
                elif player.direction == (0, 1):
                    bullet = Projectile(player.rect.x, player.rect.y + 50, player.direction, 0)
                elif player.direction == (-1, 0):
                    bullet = Projectile(player.rect.x, player.rect.y + 40, player.direction, 90)
                else:
                    bullet = Projectile(player.rect.x + 50, player.rect.y, player.direction, 270)
                bullet_group.add(bullet)
                shot_cooldown = 13
    for defender in defender_group:
        if pg.sprite.spritecollide(defender, enemy_bullet_group, True):
            defender.kill()
        if defender.shot_cooldown == 0:
            bullet = Projectile(defender.rect.x + 25, defender.rect.y, (0, -1), 0)
            bullet_group.add(bullet)
            defender.shot_cooldown = 60
    bullet_group.update()
    enemy_bullet_group.update()
    for enemy in enemy_group:
        hp = enemy.update(hp)
    enemy_bow_group.update()
    for defender in defender_group:
        defender.update(defender.rect.x, defender.rect.y)
    draw_text(f"hp: {hp}", font, black, 20, 20)
    draw_text(f"money: {money}", font, black, 780, 20)
    draw_text(f"score: {score}", font, black, 780, 60)
    draw_text("SHOP", button_font, black, 900, 705)

    if hp <= 0:
        hp, money, player, score = reset_game()

    pg.display.update()

pg.quit()