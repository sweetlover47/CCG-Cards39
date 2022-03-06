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

    def __init__(self, owner_id):
        self.owner_id = owner_id

    def level_up(self):
        self.current_level = self.current_level + 1
        self.health = self.stats[self.current_level][0]
        self.attack = self.stats[self.current_level][1]
        if self.skill is not None:
            self.skill = self.stats[self.current_level][2]


class IBattleCard:
    current_health: int
    current_attack: int
    current_skill: int

    def do_attack(self, target_card):
        target_card.was_attacked(-1, self.current_attack)

    def was_attacked(self, attacking_card, damage):
        self.current_health = max(0, self.current_health - damage)

    def use_skill(self, value, **kwargs):
        pass

    def accept_skill(self, func):
        func(self)

    def is_alive(self):
        return self.current_health == 0


class Elf(ICard):
    id = 1
    card_type = CardType.RANGE
    stats = {1: (6, 3), 2: (7, 4)}
    current_level = 1
    max_level = 2
    health = stats[current_level][0]
    attack = stats[current_level][1]


class BattleElf(Elf, IBattleCard):
    current_health = Elf.health
    current_attack = Elf.attack

    def do_attack(self, target_card):
        target_card.was_attacked(self, self.current_attack)  # TODO target needs constructor for battle


class Treant(ICard):
    id = 2
    card_type = CardType.MELEE
    stats = {1: (10, 3, 0), 2: (11, 4, 0)}
    current_level = 1
    max_level = 2
    health = stats[current_level][0]
    attack = stats[current_level][1]


class BattleTreant(Treant, IBattleCard):
    current_health = Treant.health
    current_attack = Treant.attack

    def do_attack(self, target_card):
        target_card.was_attacked(self, self.current_attack)  # TODO target needs constructor for battle

    def was_attacked(self, attacking_card, damage):
        damage = self.use_skill(damage, card_type=attacking_card.__getattribute__('card_type'))
        # attack_card.accept_skill(lambda: damage) # TODO target needs constructor for battle
        self.current_health = max(0, self.current_health - damage)

    def use_skill(self, value, **kwargs):
        return value // 2 if CardType.MELEE in kwargs.values() else value


class Lifestealer(ICard):
    id = 3
    card_type = CardType.RANGE
    stats = {1: (6, 3, 2), 2: (7, 4, 2)}
    current_level = 1
    max_level = 2
    health = stats[current_level][0]
    attack = stats[current_level][1]
    skill = stats[current_level][2]


class BattleLifestealer(Lifestealer, IBattleCard):
    current_health = Lifestealer.health
    current_attack = Lifestealer.attack
    current_skill = Lifestealer.skill

    def do_attack(self, target_card):
        target_card.was_attacked(self, self.current_attack)  # TODO target needs constructor for battle
        self.use_skill(self.current_skill)

    def use_skill(self, value, **kwargs):
        self.current_health = self.current_health


