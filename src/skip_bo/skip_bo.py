import dataclasses
import itertools
from random import Random

import numpy as np


@dataclasses.dataclass
class GameConfigs:
    max_card_value = 12
    nr_hand_cards = 5
    nr_play_field = 4
    nr_discard_piles = 4

    # debug rules
    max_discard_pile_size = 6


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

    def deal_cards(self):
        for n in range(20 if len(self.players) == 2 else 30):
            for player in self.players:
                player.deal_stock_card(self.stock.pop())

    def play_round(self):
        # todo to be replaced by step
        for player in self.players:
            self.deal_player_cards(player)
            player.play_round(self)

        self.clear_play_fields()

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
                [self.discard_stock.push(field.pop()) for _ in range(GameConfigs.max_card_value)]

    def step(self, player_id, action_id):
        ...
        # player plays stock card
        # player plays hand card
        # player discards card
        moves = {
            0: lambda game, player: player.play_stock_card(game, 0),
            1: lambda game, player: player.play_stock_card(game, 1),
            2: lambda game, player: player.play_stock_card(game, 2),
            3: lambda game, player: player.play_stock_card(game, 3),
        }
        move_moves = {
            0: lambda game, player: player.play_stock_card(game, 0),
        }

        moves[action_id](self, self.players[player_id])


    def last(self):
        ...

    def observe(self):

        return

    @staticmethod
    def possible_moves():
        """ Possible moves:

        1. from player stock to one of the field piles (4 moves)
        2. from player hand to one of the field piles (5*4 moves)
        3. from player hand to one of the discard piles (5*4 moves)

        :return:
        """
        return np.zeros(4 + 5 * 4 + 5 * 4, "int8")

    def legal_moves(self, player):
        """
         0:4  -> play player stock to field
         4:24 -> hand card to field
        24:48 -> hand card to discard pile

        :param player:
        :return:
        """
        legal_moves = self.possible_moves()
        for i, combi in enumerate([
            *itertools.product([player.stock_card], self.play_fields),
            *itertools.product(player.hand_cards, self.play_fields)
        ]):
            if combi[0] == combi[1].accepts or combi[0] == "X":
                legal_moves[i] = 1

        legal_moves[-20:] = 1  # discard to this pile is always allowed.

        return legal_moves


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

    def play_round(self, game):
        # todo: add moves AND/OR make human interface
        # 1. add card from stock to field
        for field in game.play_fields:
            if self.stock.top_card in {field.accepts, "X"}:
                field.push(self.stock.pop())

        # 2. add card from hand to field
        for card, field in itertools.product(self.hand, game.play_fields):
            if card.value in {field.accepts, "X"}:
                field.push(card.pop())

        # 3. when hand is empty, take 5 new cards
        # when build_pile is full, add to discard_stock

        for card in self.hand:
            if not card.is_empty():
                self.discard_card(card.pop())
                break
        else:  # no break
            print("player hand was empty")

    def discard_card(self, hand_idx, pile_idx):
        self.discard_piles[pile_idx].push(self.hand[hand_idx].pop())

    def play_stock_card(self, game, field_idx):
        game.play_fields[field_idx].push(self.stock.pop())

    def play_hand_card(self, game, hand_idx, field_idx):
        game.play_fields[field_idx].push(self.hand[hand_idx].pop())


class GameStock:

    def __init__(self):
        self.cards = [i + 1 for i in range(GameConfigs.max_card_value)] * 12 + ['X'] * 12

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return f"Stock with {len(self)} cards"

    def pop(self):
        return self.cards.pop()

    def shuffle(self, seed="31415"):
        Random(seed).shuffle(self.cards)

    def refill(self, cards: list):
        self.cards.extend(cards)
        self.shuffle()


class PlayerStock:
    def __init__(self):
        self.cards = []

    def __str__(self):
        return f"Player stock with {len(self.cards)} cards."

    def __len__(self):
        return len(self.cards)

    @property
    def top_card(self):
        return self.cards[-1]

    def pop(self):
        return self.cards.pop()

    def deal_push(self, card):
        self.cards.append(card)


class BuildPile:

    def __init__(self):
        self.cards = []

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return f"{self.top_card:>2}" if self.top_card else "  "

    @property
    def top_card(self):
        return len(self.cards)

    @property
    def accepts(self):
        return self.top_card + 1

    def pop(self):
        return self.cards.pop()

    def push(self, card):
        if card in {self.accepts, "X"} and self.top_card < GameConfigs.max_card_value:
            self.cards.append(card)
        else:
            raise IllegalMove("Not allowed to push this card.")


class DiscardPile:
    def __init__(self):
        self.cards = []

    def __str__(self):
        return f"{self.top_card:>2}" if self.top_card else "  "

    @property
    def top_card(self):
        return self.cards[-1] if len(self.cards) else 0

    def pop_all(self):
        return [self.cards.pop() for _ in range(len(self.cards))]

    def push(self, card):
        if len(self.cards) < GameConfigs.max_discard_pile_size:
            self.cards.append(card)
        else:
            raise IllegalMove("Artificial rule: keep discard piles small.")

    def observe(self):
        return self.cards[-3]


class HandCard:
    def __init__(self):
        self._number = 0

    def __str__(self):
        return f"{self._number:>2}" if self._number else "  "

    @property
    def value(self):
        return self._number

    def is_empty(self):
        return self._number == 0

    def pop(self):
        n = self._number
        self._number = 0
        return n

    def push(self, n):
        if self._number:
            raise IllegalMove()
        self._number = n


class IllegalMove(Exception):
    pass


if __name__ == "__main__":
    main_game = SkipBoGame(number_of_players=2)
    main_game.start()
