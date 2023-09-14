from skip_bo.settings import GameConfigs
from skip_bo.stocks import PlayerStock, HandCard, DiscardPile
from skip_bo.erors import IllegalMove


class Player:
    def __init__(self, name: str = "0"):
        self.name = name
        self.stock = PlayerStock()
        self.hand = [HandCard() for _ in range(GameConfigs.nr_hand_cards)]
        self.discard_piles = [DiscardPile() for _ in range(GameConfigs.nr_discard_piles)]

    def __str__(self):
        return f"Player {self.name}"

    @property
    def stock_card(self):
        return self.stock.top_card

    @property
    def hand_cards(self):
        return [card.value for card in self.hand]

    @property
    def discard_cards(self):
        return [card.top_card for card in self.discard_piles]

    def deal_stock_card(self, card):
        self.stock.deal_push(card)

    def deal_hand_card(self, card):
        for hand_card in self.hand:
            if hand_card.is_empty():
                hand_card.push(card)
                break
        else:  # no break
            raise IllegalMove("Dealt card to many")

    def is_finished(self):
        return len(self.stock) == 0

    def play_stock_card(self, game, field_idx):
        game.play_fields[field_idx].push(self.stock.pop())

    def play_hand_card(self, game, hand_idx, field_idx):
        game.play_fields[field_idx].push(self.hand[hand_idx].pop())

    def discard_card(self, hand_idx, pile_idx):
        self.discard_piles[pile_idx].push(self.hand[hand_idx].pop())
