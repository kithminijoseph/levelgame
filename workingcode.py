import pygame
from pygame.locals import *
import pickle

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 700
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mini's Adventures")
a = pygame.image.load('heart.png')
pygame.display.set_icon(a)

tile_size = 50
game_over = 0
main_menu = True
level = 1

bg_img = pygame.image.load('sky.png')
cg_img = pygame.image.load('cloud1.png')
dg_img = pygame.image.load('cloud2.png')
eg_img = pygame.image.load('cloud3.png')
fg_img = pygame.image.load("heartcloud1.png")
gg_img = pygame.image.load("heartcloud2.png")
hg_img = pygame.image.load("heartcloud3.png")
ig_img = pygame.image.load('pinkheartcloud1.png')
jg_img = pygame.image.load("pinkheartcloud2.png")
kg_img = pygame.image.load("pinkheartcloud3.png")
start_img = pygame.image.load("start.png")
end_img = pygame.image.load("quit.png")
restart_img = pygame.image.load('restart.png')
kithmini_img = pygame.image.load('KITHMINI.png')
strawberry_img = pygame.image.load("strawberry.png")
dead_image = pygame.image.load("dead_img.png")


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)

        return action


class Player():
    score = 0

    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5

        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] or key[pygame.K_UP] and self.jumped == False:
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_p]: #pink clouds
                screen.blit(ig_img, (0, 0))
                screen.blit(jg_img, (550, 100))
                screen.blit(kg_img, (200, 200))


                pygame.display.update()
            if key[pygame.K_LEFT]:
                dx -= 5
            if key[pygame.K_RIGHT]:
                dx += 5
 
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            self.in_air = True
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1

            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1

            for strawberryFound in pygame.sprite.spritecollide(self, strawberry_group, False):
                Player.score += 1
                strawberry_group.remove(strawberryFound)

            for megastrawberryFound in pygame.sprite.spritecollide(self, megastrawberry_group, False):
                Player.score += 10
                megastrawberry_group.remove(megastrawberryFound)
            self.rect.x += dx
            self.rect.y += dy


        elif game_over == -1:
            dead = pygame.transform.scale(dead_image, (140, 150))
            self.image = dead
            if self.rect.y > 200:
                self.rect.y -= 5

        screen.blit(self.image, self.rect)
        return game_over

    def reset(self, x, y):
        kithmini = pygame.transform.scale(kithmini_img, (75, 100))
        self.image = kithmini
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.in_air = True


class World():
    def __init__(self, data):
        self.tile_list = []

        dirt_img = pygame.image.load('grassblock.png')
        grass_img = pygame.image.load('gold.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    blob_group.add(blob)
                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                if tile == 7:
                    strawberry = Strawberry(col_count * tile_size, row_count * tile_size + 15)
                    strawberry_group.add(strawberry)
                if tile == 8:
                    megastrawberry = MegaStrawberry(col_count * tile_size, row_count * tile_size + 15)
                    megastrawberry_group.add(megastrawberry)

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('ninjafrog.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Strawberry(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('strawberry.png')
        self.image = pygame.transform.scale(img, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class MegaStrawberry(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('raspberry.png')
        self.image = pygame.transform.scale(img, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

world_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [3, 7, 0, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 7, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0],
    [0, 0, 0, 0, 0, 0, 8, 0, 0, 1, 6, 6, 1, 0],
    [0, 7, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 7, 0, 0, 0, 1, 0, 7, 0, 0, 7],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 6, 6, 1],
    [0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 6, 6, 6, 6, 1, 1, 1, 1, 1],
]

player = Player(100, screen_height - 150)

blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
strawberry_group = pygame.sprite.Group()
megastrawberry_group = pygame.sprite.Group()

world = World(world_data)


restart = pygame.transform.scale(restart_img, (130, 100))
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart)
start = pygame.transform.scale(start_img, (250, 250))
start_button = Button(screen_width // 2 - 350, screen_height // 2, start)
exit = pygame.transform.scale(end_img, (200, 200))
exit_button = Button(screen_width // 2 + 160, screen_height // 2, exit)

run = True
while run:

    clock.tick(fps)

    screen.blit(bg_img, (0, 0))
    screen.blit(cg_img, (5, 10))
    screen.blit(dg_img, (5, 10))
    screen.blit(eg_img, (5, 10))
    screen.blit(fg_img, (0, 0))
    screen.blit(gg_img, (550, 100))
    screen.blit(hg_img, (200, 200))
    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:
        world.draw()

        if game_over == 0:
            blob_group.update()

        blob_group.draw(screen)
        lava_group.draw(screen)
        strawberry_group.draw(screen)
        megastrawberry_group.draw(screen)

        game_over = player.update(game_over)
        if game_over == -1:
            if restart_button.draw():
                player.reset(100, screen_height - 130)
                game_over = 0

        if Player.score >= 1:
            font = pygame.font.SysFont("consolas", 30)
            render = font.render(str(Player.score), True, [252, 3, 102])
            x, y = screen.get_size()
            x2 = render.get_width()
            screen.blit(render, ((x + x2) * 0.5, y * 0.1))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
