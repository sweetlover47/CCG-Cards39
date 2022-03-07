from enum import Enum


class CardPosition(Enum):
    LEFT_FRONT = 1
    LEFT_REAR = 2
    RIGHT_FRONT = 3
    RIGHT_REAR = 4


class GameManager:
    decks = {}
    positions = {}

    def add_deck(self, deck):
        for _card in deck:
            self.decks[len(self.decks)] = _card
        # TODO check is correct positions for order in self.decks
        self.positions.update(dict(zip([k for k, v in self.decks.items() if v in deck],
                                       [CardPosition.LEFT_FRONT,
                                        CardPosition.LEFT_REAR,
                                        CardPosition.RIGHT_FRONT,
                                        CardPosition.RIGHT_REAR])))

    def move(self, card_id, target_card_id):
        self.decks[card_id].do_attack(self.decks[target_card_id])
        self.check_alive()

    def check_alive(self):
        for _id, _card in self.decks.items():
            if _card.is_alive():
                self.decks[_id] = None
