import pygame
import os
import sys

from random import choice, randint

pygame.init()
pygame.display.set_caption('Don`t Wake Them Up')
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1020
screen = pygame.display.set_mode(WINDOW_SIZE)
FPS = 30
clock = pygame.time.Clock()


def load_image(name, directory='', color_key=None):
    fullname = os.path.join('data', 'photos', directory, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден.")
        print(f"Скачайте все файлы, чтобы запустить игру.")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def new_level_screen():
    if open("data/level_info", encoding="utf8").read()[0] != '5':
        pygame.display.update()
        pygame.time.delay(2000)
        font = pygame.font.Font('data/Zaychik-Regular.ttf', 100)
        name_rendered = font.render(f'УРОВЕНЬ {open("data/level_info", encoding="utf8").read()[0]}',
                                    True, (193, 154, 107))
        font = pygame.font.Font('data/Zaychik-Regular.ttf', 40)
        if game.level_settings[4] != 0:
            task = font.render(f'НАЙДИТЕ ЗАПИСОК: {game.level_settings[4]}', True, (193, 154, 107))
            screen.blit(task, (830, 600))
        else:
            task = font.render('ТАМ, ГДЕ ЗАКРЫТАЯ ДВЕРЬ', True, (193, 154, 107))
            screen.blit(task, (800, 600))
        screen.blit(name_rendered, (800, 490))
        pygame.display.update()
        pygame.time.delay(5000)
        return
    else:
        pygame.display.update()
        font = pygame.font.Font('data/Zaychik-Regular.ttf', 100)
        name_rendered = font.render('ВЫ ВЫИГРАЛИ', True, (193, 154, 107))
        font = pygame.font.Font('data/Zaychik-Regular.ttf', 30)
        game_rendered = font.render('НЕ БУДИ - the game by shklyaev platon', True, (193, 154, 107))
        tap = font.render('нажми, чтобы выйти', True, (193, 154, 107))
        pygame.time.delay(2000)
        screen.blit(name_rendered, (730, 450))
        screen.blit(game_rendered, (750, 550))
        screen.blit(tap, (840, 800))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    open("data/level_info", 'w', encoding="utf8").write('1')
                    pygame.quit()
                    exit()


def start_screen():
    girl = pygame.transform.flip(load_image('GirlGhost.png'), True, False)
    fon = load_image('menu.png')
    screen.blit(fon, (0, 140))
    screen.blit(girl, (1600, 630))
    font = pygame.font.Font('data/Zaychik-Regular.ttf', 150)
    name_rendered = font.render('НЕ БУДИ', True, (193, 154, 107))
    font = pygame.font.Font('data/Zaychik-Regular.ttf', 100)
    play_rendered = font.render('ИГРАТЬ', True, (115, 66, 34))
    font = pygame.font.Font('data/Zaychik-Regular.ttf', 100)
    settings_rendered = font.render('НАСТРОЙКИ', True, (115, 66, 34))
    screen.blit(name_rendered, (180, 250))
    screen.blit(play_rendered, (270, 530))
    screen.blit(settings_rendered, (200, 650))

    levels = False

    pygame.mixer.music.load('data/music.mp3')
    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(270, 270 + play_rendered.get_rect().w) and \
                        event.pos[1] in range(530, 530 + play_rendered.get_rect().h):
                    if int(open("data/level_info", encoding="utf8").read()[0]) == 1:
                        pygame.mixer.music.stop()
                        return
                    else:
                        levels = True
                        font = pygame.font.Font('data/Zaychik-Regular.ttf', 50)
                        new = font.render('НОВАЯ ИГРА', True, (115, 66, 34))
                        download = font.render('ПРОДОЛЖИТЬ ПРОШЛУЮ', True, (115, 66, 34))
                        screen.blit(new, (540, 520))
                        screen.blit(download, (540, 580))
                if event.pos[0] in range(200, 200 + settings_rendered.get_rect().w) and \
                        event.pos[1] in range(650, 650 + settings_rendered.get_rect().h):
                    font = pygame.font.Font('data/Zaychik-Regular.ttf', 35)
                    wasd = font.render('WASD - передвижение игрока', True, (115, 66, 34))
                    tap_e = font.render('щелчок мыши или кнопка "E"', True, (115, 66, 34))
                    tap_e2 = font.render('для взаимодействия с предметами', True, (115, 66, 34))
                    screen.blit(wasd, (195, 760))
                    screen.blit(tap_e, (190, 810))
                    screen.blit(tap_e2, (145, 840))
                if levels:
                    if event.pos[0] in range(540, 700) and event.pos[1] in range(520, 550):
                        open("data/level_info", 'w', encoding="utf8").write('1')
                        pygame.mixer.music.stop()
                        return
                    if event.pos[0] in range(540, 840) and event.pos[1] in range(580, 610):
                        pygame.mixer.music.stop()
                        return

        pygame.display.flip()
        clock.tick(FPS)


PLAYING = 'start'


while True:
    if PLAYING == 'start' or PLAYING == 'lose':
        PLAYING = 'ok'
        screen.fill((0, 0, 0))
        start_screen()


    class On_screen(pygame.sprite.Sprite):

        def __init__(self, name, x, y):
            super().__init__(interface_sprites)
            self.image = load_image(name, '')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y


    class Room(pygame.sprite.Sprite):
        CODING = {}
        floor = 0

        def __init__(self, name, coord, lightning, border=False):
            super().__init__(all_sprites)

            if border:
                if name == 'teleport':
                    self.add(teleport_sprite)
                    self.image = pygame.Surface((1, abs(coord[3])), pygame.SRCALPHA)
                    self.rect = pygame.Rect(coord[0], coord[1], coord[2], coord[3])
                if name == 'wall':
                    self.add(border_sprite)
                    self.image = pygame.Surface((1, abs(coord[3])), pygame.SRCALPHA)
                    self.rect = pygame.Rect(coord[0], coord[1], coord[2], coord[3])
                if name == 'event':
                    self.add(event_border)
                    self.image = pygame.Surface((802, 802), pygame.SRCALPHA)
                    self.rect = pygame.Rect(coord[0], coord[1], coord[0] + 802, coord[1] + 802)
            else:
                if lightning is True:
                    directory = 'light_photos'
                elif lightning is False:
                    directory = 'dark_photos'
                else:
                    directory = ''
                if name == 'elevator.png' or name == '#.png':
                    self.add(elevator_sprite)
                elif name == 'fire.png':
                    self.add(fireplace_sprites)
                else:
                    self.add(house_sprites)
                self.image = load_image(name, directory if 'interior' not in name else 'interior')
                self.house = self.image
                self.rect = self.house.get_rect()
                self.rect.x, self.rect.y = coord

        def image_size(self):
            return self.rect.w, self.rect.h

        def elevator(self, coord):
            all_ap = None
            for j in all_sprites:
                all_ap = j
                break
            if coord == 'w':
                num = -802
            else:
                num = 802
            if (pygame.sprite.spritecollideany(hero, elevator_sprite) and abs(all_ap.rect.y) // 690 == self.floor) \
                    and all_ap.rect.y - num in range(-int(game.h) + 802, 110):
                for spr in all_sprites:
                    spr.rect.y -= num
                for spr in monsters_sprites:
                    spr.rect.y -= num
                game.y -= num
                for spr in elevator_sprite:
                    spr.rect.y += num
                if game.level != 1:
                    if coord == 'w':
                        game.MAP[self.floor][game.MAP[self.floor].index('elevator.png')] = '#.png'
                        game.MAP[self.floor - 1][game.MAP[self.floor - 1].index('#.png')] = 'elevator.png'
                        self.floor -= 1
                    else:
                        game.MAP[self.floor][game.MAP[self.floor].index('elevator.png')] = '#.png'
                        game.MAP[self.floor + 1][game.MAP[self.floor + 1].index('#.png')] = 'elevator.png'
                        self.floor += 1

        def is_free(self, num):
            hero.rect.x -= num
            if pygame.sprite.spritecollideany(hero, border_sprite):
                hero.rect.x += num
            else:
                hero.rect.x += num
                for sprite in all_sprites:
                    sprite.rect.x += num
                game.x += num

        def render(self, num):
            self.is_free(num)


    class Hero(pygame.sprite.Sprite):
        hero = load_image('GirlPhoto.PNG')  # изображение размером 300*300!
        SIDE = True
        new_side = True

        def __init__(self):
            super().__init__(hero_sprites)
            self.image = self.hero
            self.rect = self.hero.get_rect()
            self.rect.x = WINDOW_WIDTH // 2 - self.rect.w // 2
            self.rect.y = 570

        def move(self):
            if pygame.key.get_pressed()[pygame.K_a]:
                room.render(10)
                self.new_side = False
            if pygame.key.get_pressed()[pygame.K_d]:
                room.render(-10)
                self.new_side = True
            if self.new_side != self.SIDE:
                self.SIDE = self.new_side
                self.image = pygame.transform.flip(self.image, True, False)


    class Enemy(pygame.sprite.Sprite):
        enemy = load_image(choice(['ghost2.png', 'GirlGhost.png', 'MonsterGhost.png']))

        def __init__(self, x, y, right=True):
            super().__init__(all_sprites)

            self.add(monsters_sprites)
            self.right = right
            self.image = self.enemy
            self.rect = self.enemy.get_rect()
            self.rect.x = x
            self.rect.y = y

        def update(self):
            if game.LIGHTNING is True and len(monsters_sprites) != 0:
                game.LIGHTNING = False
                game.house_builder()

            if hero.rect.y in range(self.rect.y, self.rect.y + 400):
                if hero.rect.x > self.rect.x:
                    if self.right is False:
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.right = True
                    self.rect.x += 12
                else:
                    if self.right is True:
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.right = False
                    self.rect.x -= 12
            else:
                if self.right is True:
                    self.rect.x += 9
                else:
                    self.rect.x -= 9
                if pygame.sprite.spritecollideany(self, border_sprite):
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.right = not self.right
            if pygame.sprite.spritecollideany(hero, monsters_sprites):
                game.TIME -= 50
                self.kill()


    class Pictures(pygame.sprite.Sprite):

        def __init__(self):
            super().__init__(all_sprites)

            self.add(picture_sprites)
            coord = self.picture_piece()
            self.image = load_image("paper.png")
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = coord[0] - self.rect.w // 2, coord[1] + 100

        def picture_piece(self):
            coord = ()
            while coord == ():
                for i, sprite in enumerate(house_sprites):
                    if i > 2:
                        if randint(1, 10) == randint(1, 10):
                            coord = (sprite.rect.x + sprite.rect.w // 2, choice([510, 1312, 2114, 2916, 3718, 4520]
                                                                                [:Game.level_settings[0]]))
            return coord


    class Game:
        LIGHTNING = True
        IN_ROOM = True
        EVENT = [None]
        MAP = []
        LEVELS = {1: [1, 10, '', 240, 1, 1], 2: [2, 8, '', 240, 1, 1], 3: [3, 8, 'ELECTRIC', 360, 0, 2],
                  4: [5, 8, 'PRE-FINAL', 480, 3, 3], 5: [6, 10, 'FINAL', 600, 4, 4]}
        level = int(open("data/level_info", encoding="utf8").read()[0])
        level_settings = LEVELS[level]

        round_events = {'done': False, 'monsters': False, 'timer': 0, 'fire': False, 'fire_s': False if level < 4 else True,
                        'm_time': 0}

        def __init__(self, game_hero, game_room):

            self.TIME = self.level_settings[3]
            self.FIRE = self.level_settings[3] if self.level != 3 else 0
            self.PICTURES = self.level_settings[4]
            self.tasks = int(self.level_settings[5])
            self.done_tasks = 0

            self.game_hero = game_hero
            self.game_room = game_room
            self.w, self.h = 0, WINDOW_HEIGHT / 2 - 802 / 2
            self.x, self.y = 0, 0
            self.frame = WINDOW_HEIGHT / 2 - 802 / 2

            if self.level == 3:
                self.LIGHTNING = False
            if self.level > 3:
                On_screen('fire_tap.jpg', 1065, 15)

            self.half_photos_names = self.interior_names()
            self.MAP = self.map_maker(self.level_settings[0], self.level_settings[1])
            self.house_builder()
            On_screen('2972528.png', 938, 15)

            for i in range(self.PICTURES):
                Pictures()

        def display_resolution(self):
            pygame.draw.rect(screen, pygame.Color('black'), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT / 2 - 401))
            pygame.draw.rect(screen, pygame.Color('black'), (0, WINDOW_HEIGHT - (WINDOW_HEIGHT / 2 - 401),
                                                             WINDOW_WIDTH, WINDOW_HEIGHT / 2 - 401))

        def interior_names(self):
            all_files = [files for root, dirs, files in os.walk("data/photos/interior")][0]
            return [list(filter(lambda x: x[:3] == '401', all_files)), list(filter(lambda x: x[:3] != '401', all_files))]

        def map_maker(self, floors, rooms):
            self.MAP = [list('' for _ in range(rooms)) for _ in range(floors)]
            hp_colvo = randint(1, (rooms - 4) // 4) * 2  # количество спрайтов из папки interior
            sprite_coord401, sprite_coord802 = [], []  # координаты дизайн-спрайтов с шириной 401 и 802
            elevator_coord = randint(1, rooms - 2)
            photos = list(filter(lambda x: 'fence' not in x and 'corner' not in x and 'elevator' not in x and '#' not in x
                                           and 'fire' not in x and 'key' not in x,
                                 [files for root, dirs, files in os.walk("data/photos/dark_photos")][0]))
            for i in range(floors):
                if len(sprite_coord401) == 0:
                    places = [i for i in range(1, rooms)]
                    for j in range(hp_colvo):
                        a = randint(0, len(places) - 1)
                        sprite_coord401.append(places[a])
                        del places[a]
                    for h in range(hp_colvo):
                        a = randint(1, len(places) - 1)
                        sprite_coord802.append(places[a])
                        del places[a]
                for q in sprite_coord401:
                    self.MAP[i][q] = choice(self.half_photos_names[0])
                for w in sprite_coord802:
                    self.MAP[i][w] = choice(self.half_photos_names[1])
                for k in range(len(self.MAP[i])):
                    if self.MAP[i][k] == '':
                        self.MAP[i][k] = choice(photos)
                self.MAP[i][-1] = choice(['cornerEmR.png', 'cornerLaR.png'])
                if i == 0:
                    self.MAP[i][0] = choice(['cornerDoor.png', 'cornerDoorL.png'])
                    if floors != 1:
                        self.MAP[i][elevator_coord] = 'elevator.png'
                else:
                    self.MAP[i][0] = choice(['cornerEmL.png', 'cornerLaL.png'])
                    self.MAP[i][elevator_coord] = '#.png'
                if self.level_settings[2] != '':
                    self.MAP[-1][-1] = 'fire.png'
                if self.level_settings[2] == 'ELECTRIC':
                    self.MAP[-1][-1] = 'fence.png'
                    for f in range(1, len(self.MAP) + 1):
                        for j in range(len(self.MAP[f])):
                            if 'interior' not in self.MAP[f][j] and 'corner' not in self.MAP[f][j] \
                                    and '#' not in self.MAP[f][j]:
                                self.MAP[f][j] = choice(['LCPkey.png', 'LPkey.png'])
                                self.EVENT = [self.MAP[f][j], f, j]
                                break
                        break

            return self.MAP

        def house_builder(self):
            all_sprites.empty()
            self.h = WINDOW_HEIGHT / 2 - 802 / 2
            for x in self.MAP:
                self.w = 0
                for i, y in enumerate(x):
                    self.game_room = Room(y, (self.x + self.w, self.y + self.h), self.LIGHTNING)
                    if y == self.EVENT[0]:
                        self.EVENT.extend((self.x + self.w, self.y + self.h))
                    self.w += self.game_room.image_size()[0]
                self.h += self.game_room.image_size()[1]

            Room('wall', (40 + self.x, -802 + self.frame + self.y, 39, self.h + 802), None, True)
            Room('wall', (self.w - 90 + self.x, 0 + self.y, self.w - 89, self.h), None, True)
            Room('MainRoom.png', (0 + self.x, -802 + self.frame + self.y), None)
            Room('wall', (1600 + self.x, 0 + self.frame + self.y, 1601, -802 + self.frame), None, True)
            Room('teleport', (40 + self.x, 0 + self.frame + self.y, 200, 802 + self.frame), None, True)
            Room('teleport', (1400 + self.x, 0 + self.frame + self.y, 1600, -802 + self.frame), None, True)
            if self.level_settings[2] == 'ELECTRIC' and 'key' in self.EVENT[0]:
                Room('event', (self.EVENT[3], self.EVENT[4]), None, True)
                Room('wall', (self.w + self.x - 802, int(self.h + self.y - 802), 802, 802), None, True)

        def e_tap(self):
            if pygame.sprite.spritecollideany(hero, teleport_sprite):
                if self.IN_ROOM:
                    self.IN_ROOM = False
                    for sprite in all_sprites:
                        sprite.rect.y += 802
                        sprite.rect.x -= 600
                    hero.rect.y += 50
                else:
                    self.IN_ROOM = True
                    for sprite in all_sprites:
                        sprite.rect.y -= 802
                        sprite.rect.x += 600
                    hero.rect.y -= 50
            elif pygame.sprite.spritecollideany(hero, fireplace_sprites):
                self.FIRE = self.level_settings[3]
                fireplace_sprites.empty()
                game.LIGHTNING = True
                game.house_builder()
                for i in monsters_sprites:
                    i.kill()
            else:
                if not self.IN_ROOM and self.done_tasks == self.tasks:
                    new_level = int(open("data/level_info", encoding="utf8").read()[0]) + 1
                    open("data/level_info", 'w', encoding="utf8").write(str(new_level))
                    global running
                    running = False

        def events(self):
            if pygame.sprite.spritecollideany(hero, event_border):
                if 'key' in self.EVENT[0]:
                    self.MAP[int(self.EVENT[1])][int(self.EVENT[2])] = self.EVENT[0].replace('key', '')
                    self.house_builder()
                    event_border.empty()
                    self.EVENT = ['Electro']
                    Room('event', (self.w + self.x - 1604, self.h + self.y - 802), None, True)
                    self.done_tasks += 1
                elif self.EVENT[0] == 'Electro':
                    self.MAP[-1][-1] = 'fire.png'
                    self.house_builder()
                    self.EVENT = ['']
                    event_border.empty()
                    for sprite in border_sprite:
                        if sprite.rect == (self.w + self.x - 802, int(self.h + self.y - 802), 802, 802):
                            sprite.kill()
                    self.done_tasks += 1
                    On_screen('fire_tap.jpg', 1065, 15)
                    self.round_events['fire_s'] = True
            if pygame.sprite.spritecollideany(hero, picture_sprites):
                for i in picture_sprites:
                    if i.rect in hero.rect:
                        i.kill()
                        self.done_tasks += 1

        def render(self):
            all_sprites.draw(screen)
            picture_sprites.draw(screen)
            hero_sprites.draw(screen)
            monsters_sprites.draw(screen)
            self.display_resolution()
            interface_sprites.draw(screen)

            self.TIME -= 0.15
            self.FIRE -= 0.25
            pygame.draw.rect(screen, 'white', (898, 70, 124, 20), 2)
            pygame.draw.rect(screen, (193, 154, 107), (900, 72, self.TIME // (self.level_settings[3] // 120), 16), 0)
            if self.round_events['fire_s'] is True:
                pygame.draw.rect(screen, 'white', (1028, 70, 124, 20), 2)
                pygame.draw.rect(screen, (200, 0, 0), (1030, 72, self.FIRE // (self.level_settings[3] // 120), 16), 0)
            if self.FIRE < 0 and self.LIGHTNING is True:
                self.LIGHTNING = False
                self.house_builder()

            if self.round_events['done'] is False:
                if self.level == 1:
                    if self.done_tasks == 1:
                        self.round_events['timer'] += 1
                        if self.round_events['timer'] == 100:
                            self.LIGHTNING = False
                            self.house_builder()
                            self.round_events['done'] = True
                elif self.level == 2:
                    if self.done_tasks == 1 and game.y == 0:
                        self.round_events['monsters'] = True
                        self.round_events['done'] = True
                        enemy.rect.x, enemy.rect.y = hero.rect.x + 2500, 570
                elif self.level == 3:
                    if self.TIME < 160 and self.round_events['monsters'] is False:
                        enemy.rect.x, enemy.rect.y = hero.rect.x + 2500, 570
                        self.round_events['monsters'] = True
                    if pygame.sprite.spritecollideany(hero, fireplace_sprites) \
                            and self.round_events['fire'] is False:
                        self.round_events['fire'] = True
                        self.round_events['timer'] = 200
                        On_screen('fire_text.png', 725, 900)
                    if self.round_events['timer'] != 0:
                        self.round_events['timer'] -= 1
                    else:
                        for i in interface_sprites:
                            if (i.rect.x, i.rect.y) == (725, 900):
                                i.kill()
                                self.round_events['done'] = True
                elif self.level == 4:
                    if (int(self.TIME) == 440 or int(self.TIME) == 350 or int(self.TIME) == 200 or int(self.TIME) == 50) \
                            and int(self.TIME) != self.round_events['m_time']:
                        Enemy(hero.rect.x + 2500, 570 * randint(1, 5))
                        self.FIRE = 0
                        self.round_events['monsters'] = True
                        self.round_events['m_time'] = int(self.TIME)
            self.game_hero.move()
            if self.round_events['monsters']:
                monsters_sprites.update()


    def main():
        global running, PLAYING
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or game.TIME < 0:
                    running = False
                    PLAYING = 'lose'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game.events()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    game.e_tap()
                if len(elevator_sprite) != 0:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                        room.elevator('w')
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                        room.elevator('s')
            screen.fill((0, 0, 0))

            game.render()

            pygame.display.flip()
            clock.tick(FPS)


    all_sprites = pygame.sprite.Group()
    border_sprite = pygame.sprite.Group()
    event_border = pygame.sprite.Group()
    teleport_sprite = pygame.sprite.Group()
    elevator_sprite = pygame.sprite.Group()
    house_sprites = pygame.sprite.Group()
    hero_sprites = pygame.sprite.Group()
    monsters_sprites = pygame.sprite.Group()
    interface_sprites = pygame.sprite.Group()
    picture_sprites = pygame.sprite.Group()
    fireplace_sprites = pygame.sprite.Group()

    hero = Hero()
    room = Room('CaL.png', (0, 0), True)
    game = Game(hero, room)
    enemy = Enemy(game.w + 1000, 570)

    running = True

    screen.fill((0, 0, 0))
    new_level_screen()
    main()

    all_sprites.empty()
    hero_sprites.empty()
    monsters_sprites.empty()
    interface_sprites.empty()
