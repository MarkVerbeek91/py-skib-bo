import itertools

from skip_bo.player import Player
from skip_bo.settings import GameConfigs
from skip_bo.stocks import BuildPile
from skip_bo.stocks import DiscardPile
from skip_bo.stocks import GameStock


class SkipBoGame:
    def __init__(self, number_of_players=2):
        self.stock = GameStock()
        self.discard_stock = DiscardPile()
        self.play_fields = [BuildPile() for _ in range(GameConfigs.nr_play_field)]
        self.players = [Player(str(i)) for i in range(number_of_players)]

    def __str__(self):
        return "Skip-Bo game"

    @property
    def field_cards(self):
        return [card.top_card for card in self.play_fields]

    def start(self):
        self.stock.shuffle()
        self.deal_cards()

    def observe(self, agent):
        """

        1. top stock card
        2. cards on play fields
        3. cards in player hand
        4. cards on top of discard pile (extension possible for top 3, 4 or 6)

        :param agent:
        :return:
        """
        # current_index = self.
        observation = [
            [self.players[agent].stock_card]
            + self.field_cards
            + self.players[agent].hand_cards
            + self.players[agent].discard_cards
        ][0]

        return observation

    def step(self, player_id, action_id):
        ...
        # player plays stock card
        # player plays hand card
        # player discards card
        moves_list = [
            lambda game, player: player.play_stock_card(game, 0),
            lambda game, player: player.play_stock_card(game, 1),
            lambda game, player: player.play_stock_card(game, 2),
            lambda game, player: player.play_stock_card(game, 3),
            lambda game, player: player.play_hand_card(game, 0, 0),
            lambda game, player: player.play_hand_card(game, 0, 1),
            lambda game, player: player.play_hand_card(game, 0, 2),
            lambda game, player: player.play_hand_card(game, 0, 3),
            lambda game, player: player.play_hand_card(game, 1, 0),
            lambda game, player: player.play_hand_card(game, 1, 1),
            lambda game, player: player.play_hand_card(game, 1, 2),
            lambda game, player: player.play_hand_card(game, 1, 3),
            lambda game, player: player.play_hand_card(game, 2, 0),
            lambda game, player: player.play_hand_card(game, 2, 1),
            lambda game, player: player.play_hand_card(game, 2, 2),
            lambda game, player: player.play_hand_card(game, 2, 3),
            lambda game, player: player.play_hand_card(game, 3, 0),
            lambda game, player: player.play_hand_card(game, 3, 1),
            lambda game, player: player.play_hand_card(game, 3, 2),
            lambda game, player: player.play_hand_card(game, 3, 3),
            lambda game, player: player.play_hand_card(game, 4, 0),
            lambda game, player: player.play_hand_card(game, 4, 1),
            lambda game, player: player.play_hand_card(game, 4, 2),
            lambda game, player: player.play_hand_card(game, 4, 3),
            lambda _, player: player.discard_card(0, 0),
            lambda _, player: player.discard_card(0, 1),
            lambda _, player: player.discard_card(0, 2),
            lambda _, player: player.discard_card(0, 3),
            lambda _, player: player.discard_card(1, 0),
            lambda _, player: player.discard_card(1, 1),
            lambda _, player: player.discard_card(1, 2),
            lambda _, player: player.discard_card(1, 3),
            lambda _, player: player.discard_card(2, 0),
            lambda _, player: player.discard_card(2, 1),
            lambda _, player: player.discard_card(2, 2),
            lambda _, player: player.discard_card(2, 3),
            lambda _, player: player.discard_card(3, 0),
            lambda _, player: player.discard_card(3, 1),
            lambda _, player: player.discard_card(3, 2),
            lambda _, player: player.discard_card(3, 3),
            lambda _, player: player.discard_card(4, 0),
            lambda _, player: player.discard_card(4, 1),
            lambda _, player: player.discard_card(4, 2),
            lambda _, player: player.discard_card(4, 3),
        ]

        moves = dict((i, x) for i, x in enumerate(moves_list))

        moves[action_id](self, self.players[player_id])

    def reset(self):
        self.__str__()

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
