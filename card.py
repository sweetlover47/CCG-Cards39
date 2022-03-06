from enum import Enum
from typing import List


class CardType(Enum):
    MELEE = 1
    RANGE = 2
    SUPPORT = 3


class ICard:
    id: int
    owner_id: int = None
    level: int
    health: int
    attack: int
    skill: int = None
    card_type: List[CardType]
    stats: dict
    current_level: int
    max_level: int

    def level_up(self):
        self.current_level = self.current_level + 1
        self.health = self.stats[self.current_level][0]
        self.attack = self.stats[self.current_level][1]


class IBattleCard:
    def do_attack(self, target, damage):
        pass

    def was_attacked(self, attacking, damage):
        pass

    def apply_skill(self, value):
        pass

    def accept_skill(self, func):
        pass


class Elf(ICard):
    id = 1
    stats = {1: (6, 3), 2: (7, 4)}
    current_level = 1
    max_level = 2
    health = stats[current_level][0]
    attack = stats[current_level][1]


class BattleElf(Elf, IBattleCard):
    current_health = Elf.health
    current_attack = Elf.attack

    def do_attack(self, target_id, damage):
        target = get_card_by_id(target_id, True)
        target.was_attacked(self, damage)

    def was_attacked(self, attacking, damage):
        self.current_health = max(0, self.current_health - damage)

    def accept_skill(self, func):
        func(self)


class Treant(ICard):
    id = 2
    stats = {1: (10, 3), 2: (11, 4)}
    current_level = 1
    max_level = 2


def get_card_by_id(id, is_battle=False):
    if id == 1:
        return Elf if not is_battle else BattleElf
    elif id == 2:
        return Treant if not is_battle else BattleTreant
