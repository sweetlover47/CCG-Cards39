import json
import os
from enum import Enum

import pygame

import card
import game_manager


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
    def __init__(self, img, pos: game_manager.CardPosition, owner_id: int):
        pygame.sprite.Sprite.__init__(self)
        self.image = img if not owner_id else pygame.transform.flip(img, True, False)
        self.rect = self.image.get_rect()
        self.rect.center = PositionCoordinates.__getattribute__(PositionCoordinates, pos.name).value
        self.rect.center = (WIDTH * owner_id + (-1) ** owner_id * self.rect.centerx,
                            HEIGHT * owner_id + (-1) ** owner_id * self.rect.centery)

    def update(self):
        pass


WIDTH = 1360
HEIGHT = 580
FPS = 10
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
gm = game_manager.GameManager()

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
        _card.owner_id)

sprite_group.add(sprites.values())

running = True
while running:
    clock.tick(FPS)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
    sprite_group.update()

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
