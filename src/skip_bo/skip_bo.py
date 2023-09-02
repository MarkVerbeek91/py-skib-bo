import time
from random import Random


class GameStock:

    def __init__(self):
        self.cards = [i + 1 for i in range(12)] * 12 + ['X'] * 12

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return f"Stock with {len(self)} cards"

    def pop(self, n=1):
        return [self.cards.pop() for _ in range(n)]

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
        return str(self.top_card)

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
            player.play_round(self)

    def is_game_finished(self):
        return any([p.is_finished() for p in self.players])

    def refill_stock(self):
        self.stock.refill(self.discard_stock.cards)
        self.discard_stock.cards = []


class Player:
    def __init__(self, name: str = "0"):
        self.name = name
        self.hand = []
        self.stock = BuildPile()
        self.discard_piles = [BuildPile() for _ in range(4)]

    def __str__(self):
        return f"Player {self.name}"

    def deal_stock_card(self, n: list):
        self.stock.push(*n)

    def play_round(self, game):
        self.refill_hand(game)

        # todo: add moves AND/OR make human interface
        # 1. add card from stock to field
        for field in game.play_fields:
            if self.stock.top_card == field.accepts:
                field.push(self.stock.pop())
        # 2. add card from hand to field
        for i, card in enumerate(self.hand):
            for field in game.play_fields:
                if card == field.accepts:
                    field.push(card)
                    self.hand[i] = None
                    card = None
        self.hand = [c for c in self.hand if c is not None]

        for i, card in enumerate(self.hand):
            for field in game.play_fields:
                if card == field.accepts:
                    field.push(card)
                    self.hand[i] = None
                    card = None
        self.hand = [c for c in self.hand if c is not None]

        # 3. when hand is empty, take 5 new cards
        # when build_pile is full, add to discard_stock

        self.discard_card(self.hand.pop())

    def refill_hand(self, game):
        try:
            self.hand.extend(game.stock.pop(5 - len(self.hand)))
        except IndexError:
            game.refill_stock()
            self.hand.extend(game.stock.pop(5 - len(self.hand)))

    def discard_card(self, card):
        # todo: add logic
        self.discard_piles[0].push(card)

    def is_finished(self):
        return len(self.stock) == 0


def display(game):
    for player in game.players:
        print_player_status(player)

    h = " ".join([f"[{str(x):>2}]" for x in game.play_fields])
    print(f"desk     : {h}")
    print("")


def print_player_status(player):
    name = player.name
    h = player.hand
    h = h + ["  "] * (5 - len(h))
    h = " ".join([f"[{x:>2}]" for x in h])
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

    for nr in range(50):
        print(f"Round    : {nr:>3}")
        # print("Before:")
        # display(main_game)
        main_game.play_round()
        # print("After:")
        display(main_game)

        # time.sleep(0.25)
