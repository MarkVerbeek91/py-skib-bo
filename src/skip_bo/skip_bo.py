import itertools
import time
from random import Random


class GameStock:

    def __init__(self):
        self.cards = [i + 1 for i in range(12)] * 12 + ['X'] * 12

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


class BuildPile:

    def __init__(self):
        self.cards = []

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return f"{self.top_card:>2}" if self.top_card else "  "

    @property
    def top_card(self):
        return self.cards[-1] if len(self.cards) else 0

    @property
    def accepts(self):
        # todo: deal with skip-bo
        return self.top_card + 1

    def pop(self):
        return self.cards.pop()

    def push(self, card):
        # todo add error checking
        return self.cards.append(card)


class IllegalMove(Exception):
    pass


class HandCard:
    def __init__(self):
        self._number = 0

    def __str__(self):
        return f"{self._number:>2}" if self._number else "  "

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


class SkipBoGame:
    def __init__(self, number_of_players=2):
        self.stock = GameStock()
        self.discard_stock = BuildPile()
        self.play_fields = [BuildPile() for _ in range(4)]
        self.players = [Player(str(i)) for i in range(number_of_players)]

    def __str__(self):
        return "Skip-bo game"

    def start(self):
        self.stock.shuffle()
        self.deal_cards()

    def deal_cards(self):
        for n in range(20 if len(self.players) == 2 else 30):
            for player in self.players:
                player.deal_stock_card(self.stock.pop())

    def play_round(self):
        for player in self.players:
            self.deal_player_cards(player)
            player.play_round(self)

    def is_game_finished(self):
        return any([p.is_finished() for p in self.players])

    def refill_stock(self):
        self.stock.refill(self.discard_stock.cards)
        self.discard_stock.cards = []

    def deal_player_cards(self, player):
        for card in player.hand:
            if card.is_empty():
                card.push(self.stock.pop())


class Player:
    def __init__(self, name: str = "0"):
        self.name = name
        self.hand = [HandCard() for _ in range(5)]
        self.stock = BuildPile()
        self.discard_piles = [BuildPile() for _ in range(4)]

    def __str__(self):
        return f"Player {self.name}"

    @property
    def number_of_hand_cards(self):
        return sum([1 for c in self.hand if not c.is_empty()])

    def deal_stock_card(self, card):
        self.stock.push(card)

    def deal_hand_card(self, card):
        for hand_card in self.hand:
            if hand_card.is_empty():
                hand_card.push(card)
                break
        else:  # no break
            raise IllegalMove("Dealt card to many")

    def play_round(self, game):
        # todo: add moves AND/OR make human interface
        # 1. add card from stock to field
        for field in game.play_fields:
            if self.stock.top_card == field.accepts:
                field.push(self.stock.pop())
        # 2. add card from hand to field
        for card, field in itertools.product(self.hand, game.play_fields):
            if card == field.accepts:
                field.push(card.pop())

        # 3. when hand is empty, take 5 new cards
        # when build_pile is full, add to discard_stock

        for card in self.hand:
            if not card.is_empty():
                self.discard_card(card.pop())
                break
        else:  # no break
            print("player hand was empty")

    def discard_card(self, card):
        # todo: add logic
        self.discard_piles[0].push(card)

    def is_finished(self):
        return len(self.stock) == 0


class ObservationSpace:
    def __init__(self):
        pass

    def space(self):
        # possible moves:
        # top card from stock to one of the fields (4 moves)
        # each card from hand to one of the field (5*4 moves)
        # each card from hand to one of the discard piles (5*4 moves)
        return self.hand_cards_to_field(range(4), range(5)),

    @staticmethod
    def hand_cards_to_field(h_idx, f_idx) -> list:
        return list(map(lambda x: (x[0], x[1]), itertools.product(h_idx, f_idx)))


class ActionMask:
    ...


class ActionSpace:
    ...


def display(game):
    for player in game.players:
        print_player_status(player)

    h = " ".join([f"[{str(x):>2}]" for x in game.play_fields])
    print(f"desk     : {h}")
    print("")


def print_player_status(player):
    name = player.name

    h = " ".join([f"[{str(x):>2}]" for x in player.hand])
    print(f"player {name} : {h}")
    h = player.discard_piles
    h = " ".join([f"[{str(x):>2}]" for x in h])
    s = player.stock.top_card
    print(f"         : {h}      [{str(s):>2}]")


if __name__ == "__main__":
    main_game = SkipBoGame()
    main_game.start()

    # while not main_game.is_game_finished():
    #     main_game.play_round()
    #     display(main_game)
    #     time.sleep(0.25)

    for nr in range(3):
        print(f"Round    : {nr:>3}")
        # print("Before:")
        # display(main_game)
        main_game.play_round()
        # print("After:")
        display(main_game)

        # time.sleep(0.25)
