from random import shuffle


class GameStock:

    def __init__(self):
        self.cards = [i + 1 for i in range(12)] * 12 + ['X'] * 12

    def __len__(self):
        return len(self.cards)

    def pop(self, n=1):
        return [self.cards.pop() for i in range(n)]

    def shuffle(self):
        shuffle(self.cards)


class BuildPile:

    def __init__(self):
        self.cards = []

    def __len__(self):
        return len(self.cards)

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
        self.play_field = [BuildPile()] * 4
        self.players = [Player()] * number_of_players

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


class Player:
    def __init__(self):
        self.hand = []
        self.stock = BuildPile()
        self.discard_piles = [BuildPile()] * 4

    def deal_stock_card(self, n):
        self.stock.push(n)

    def play_round(self, game):
        self.refill_hand(game)

        # todo: add moves AND/OR make human interface
        # add card from stock to field
        for field in game.play_field:
            if self.stock.top_card == field.accepts:
                field.push(self.stock.pop())
        # add card from hand to field
        # when hand is empty, take 5 new cards
        # when build_pile is full, add to discard_stock
        for card in self.hand:
            for field in game.play_field:
                if card == field.accepts:
                    field.push(card)

        self.discard_card(self.hand.pop())

    def refill_hand(self, game):
        self.hand.extend(game.stock.pop(5 - len(self.hand)))

    def discard_card(self, card):
        # todo: add logic
        self.discard_piles[0].push(card)

    def is_finished(self):
        return len(self.stock) == 0


if __name__ == "__main__":
    main_game = SkipBoGame()
    main_game.start()

    while not main_game.is_game_finished():
        main_game.play_round()
