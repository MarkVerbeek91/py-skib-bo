import itertools

from skip_bo.player import Player
from skip_bo.settings import GameConfigs
from skip_bo.stocks import BuildPile
from skip_bo.stocks import DiscardPile
from skip_bo.stocks import GameStock


class SkipBoGame:
    def __init__(self, number_of_players: int = 2):
        self.stock = GameStock()
        self.discard_stock = DiscardPile()
        self.play_fields = [BuildPile() for _ in range(GameConfigs.nr_play_field)]
        self.players = [Player(str(i)) for i in range(number_of_players)]

    def __str__(self) -> str:
        return "Skip-Bo game"

    @property
    def field_cards(self):
        return [card.top_card for card in self.play_fields]

    def start(self):
        self.stock.shuffle()
        self.deal_cards()

    def deal_cards(self):
        for n in range(20 if len(self.players) == 2 else 30):
            for player in self.players:
                player.deal_stock_card(self.stock.pop())

    def is_game_finished(self):
        return any([p.is_finished() for p in self.players])

    def deal_player_cards(self, player):
        for card in player.hand:
            if len(self.stock):
                self.refill_stock()

            if card.is_empty():
                card.push(self.stock.pop())

    def refill_stock(self):
        self.stock.refill(self.discard_stock.cards)
        self.discard_stock.cards = []

    def clear_play_fields(self):
        for field in self.play_fields:
            if field.top_card == GameConfigs.max_card_value:
                [
                    self.discard_stock.push(field.pop())
                    for _ in range(GameConfigs.max_card_value)
                ]

    def last(self):
        ...

    @staticmethod
    def possible_moves():
        """Possible moves:

        1. from player stock to one of the field piles (4 moves)
        2. from player hand to one of the field piles (5*4 moves)
        3. from player hand to one of the discard piles (5*4 moves)

        :return:
        """
        return [0] * (4 + 5 * 4 + 5 * 4)

    def legal_moves(self, player):
        """
         0:4  -> play player stock to field
         4:24 -> hand card to field
        24:48 -> hand card to discard pile

        :param player:
        :return:
        """
        legal_moves = self.possible_moves()
        for i, combi in enumerate(
            [
                *itertools.product([player.stock_card], self.play_fields),
                *itertools.product(player.hand_cards, self.play_fields),
            ]
        ):
            if combi[0] == combi[1].accepts or combi[0] == "X":
                legal_moves[i] = 1

        for i in range(len(legal_moves) - 20, len(legal_moves)):
            legal_moves[i] = 1  # discard to this pile is always allowed.

        return legal_moves


if __name__ == "__main__":
    main_game = SkipBoGame(number_of_players=2)
    main_game.start()
