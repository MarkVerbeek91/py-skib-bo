from random import Random

from skip_bo.erors import IllegalMove
from skip_bo.settings import GameConfigs


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
