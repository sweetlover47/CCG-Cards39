import json
import os
from enum import Enum

import pygame

import card
import game_manager

gm = game_manager.GameManager()



###########
def print_status():
    for _id, _card in gm.decks.items():
        print('ID', _id, '###', _card.__class__.__name__, ': ♥', _card.current_health, '\u2694', _card.current_attack)

###########

#################
# 140#440#920#1220 x
# 140#140#140#140# y
#################
# 140#440#920#1220 x
# 440#440#440#440# y
#################

class PositionCoordinates(Enum):
    LEFT_FRONT = (440, 140)
    LEFT_REAR = (140, 140)
    RIGHT_FRONT = (440, 440)
    RIGHT_REAR = (140, 440)


class CardSprite(pygame.sprite.Sprite):
    _card: card.ICard

    def __init__(self, img: pygame.Surface, pos: game_manager.CardPosition, _card: card.ICard):
        pygame.sprite.Sprite.__init__(self)
        self._card = _card
        self.image = img if not _card.owner_id else pygame.transform.flip(img, True, False)
        self.rect = self.image.get_rect()
        self.rect.center = PositionCoordinates.__getattribute__(PositionCoordinates, pos.name).value
        self.rect.center = (WIDTH * _card.owner_id + (-1) ** _card.owner_id * self.rect.centerx,
                            HEIGHT * _card.owner_id + (-1) ** _card.owner_id * self.rect.centery)

    def update(self):
        pass

    def choose_card(self, pos):
        if self._card.owner_id == gm.turn:
            if gm.attack_target[1] == -1:
                # If chose own card first time then it increase the sprite size
                # Also set flag choosing which card would be attacking
                print('Choose which card you would like to attack')
                self.image = pygame.transform.scale(self.image, (SPRITE_SIZE * 1.5, SPRITE_SIZE * 1.5))
                self.rect = self.image.get_rect() # TODO Extract to private method or refactor code logic
                self.rect.center = PositionCoordinates.__getattribute__(PositionCoordinates, pos.name).value
                self.rect.center = (WIDTH * self._card.owner_id + (-1) ** self._card.owner_id * self.rect.centerx,
                                    HEIGHT * self._card.owner_id + (-1) ** self._card.owner_id * self.rect.centery)
                gm.attack_target = ([k for k, v in gm.decks.items() if v == self._card][0], -1)
            else:
                # Chose own card second time as target
                print('If I can heal than I do it')
        elif gm.attack_target[0] != -1:
            # Chose enemy's card as target
            gm.attack_target = (gm.attack_target[0], [k for k, v in gm.decks.items() if v == self._card][0])
            gm.move()
            self.image = pygame.transform.scale(self.image, (SPRITE_SIZE / 1.5, SPRITE_SIZE / 1.5)) # TODO It changes target card size, need to resize previous card from gm.attack_target[0]
            self.rect = self.image.get_rect()
            self.rect.center = PositionCoordinates.__getattribute__(PositionCoordinates, pos.name).value
            self.rect.center = (WIDTH * self._card.owner_id + (-1) ** self._card.owner_id * self.rect.centerx,
                                HEIGHT * self._card.owner_id + (-1) ** self._card.owner_id * self.rect.centery)
        else:
            print('It\'s not your card!')
        print_status()


WIDTH = 1360
HEIGHT = 580
FPS = 10
SPRITE_SIZE = 240
background = [120, 120, 120]
sprite_dir = os.path.join(os.path.dirname(__file__), 'sprite')

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(background)
pygame.display.set_caption('Card Heroes 3.0')
clock = pygame.time.Clock()

# sprite_elf = pygame.image.load(os.path.join(sprite_dir, 'elf.png')).convert()
# sprite_treant = pygame.image.load(os.path.join(sprite_dir, 'treant.png')).convert()

sprite_group = pygame.sprite.Group()

gm.add_deck([card.BattleTreant(0), card.BattleElf(0), card.BattleTreant(0)])
gm.add_deck([card.BattleElf(1), card.BattleTreant(1)])

sprites = {}

with open('card_sprites.json', 'r') as card_sprites_f:
    card_sprites = json.load(card_sprites_f)
card_sprites = {it['name']: it['img'] for it in card_sprites}

for _id, _card in gm.decks.items():
    sprites[(gm.positions[_id], _card.owner_id)] = CardSprite(
        pygame.image.load(card_sprites[_card.__class__.__name__[6:]]).convert(),
        gm.positions[_id],
        _card)

sprite_group.add(sprites.values())

gm.turn = 0
running = True
while running:
    clock.tick(FPS)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.MOUSEBUTTONUP:
            for sp in sprite_group:
                if sp.rect.collidepoint(pygame.mouse.get_pos()):
                    sp.choose_card(*[k[0] for k, v in sprites.items() if v == sp])

    sprite_group.update()

    screen.fill(background)
    sprite_group.draw(screen)
    pygame.display.flip()

pygame.quit()

# class Player(pygame.sprite.Sprite):
#     speed: int
#
#     def __init__(self, sprite, pos, speed):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = sprite
#         self.rect = self.image.get_rect()
#         self.rect.center = pos
#         self.speed = speed
#
#     def update(self):
#         self.rect.x += self.speedx
#         if self.rect.left > WIDTH:
#             self.rect.right = 0
#
#
# all_sprites.add([Player(sprite_elf, (120, 125), 5),
#                  Player(sprite_treant, (240, 370), 1)])

# running = True
# while running:
#     clock.tick(FPS)
#     for e in pygame.event.get():
#         if e.type == pygame.QUIT:
#             running = False
#
#     all_sprites.update()
#
#     screen.fill(background)
#     all_sprites.draw(screen)
#
#     pygame.display.flip()
#
# pygame.quit()
