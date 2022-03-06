import card


class GameManager:
    decks = {}

    def add_deck(self, deck):
        for _card in deck:
            self.decks[len(self.decks)] = _card

    def move(self, card_id, target_card_id):
        self.decks[card_id].do_attack(self.decks[target_card_id])
