"""Player class for Skip-Bo game."""
from skip_bo.errors import IllegalMove
from skip_bo.settings import GameConfigs
from skip_bo.stocks import DiscardPile
from skip_bo.stocks import HandCard
from skip_bo.stocks import PlayerStock


class Player:
    def __init__(self, name: str = "0"):
        self.name = name
        self.stock = PlayerStock()
        self.hand = [HandCard() for _ in range(GameConfigs.nr_hand_cards)]
        self.discard_piles = [
            DiscardPile() for _ in range(GameConfigs.nr_discard_piles)
        ]

    def __str__(self) -> str:
        return f"Player {self.name}"

    @property
    def stock_card(self) -> int:
        return self.stock.top_card

    @property
    def hand_cards(self) -> list[int]:
        return [card.value for card in self.hand]

    @property
    def discard_cards(self) -> list[int]:
        return [card.top_card for card in self.discard_piles]

    def deal_stock_card(self, card: int) -> None:
        self.stock.deal_push(card)

    def deal_hand_card(self, card) -> None:
        for hand_card in self.hand:
            if hand_card.is_empty():
                hand_card.push(card)
                break
        else:  # no break
            raise IllegalMove("Dealt card to many")

    def is_finished(self) -> bool:
        return len(self.stock) == 0

    def play_stock_card(self, game, field_idx) -> None:
        game.play_fields[field_idx].push(self.stock.pop())

    def play_hand_card(self, game, hand_idx, field_idx) -> None:
        game.play_fields[field_idx].push(self.hand[hand_idx].pop())

    def discard_card(self, hand_idx, pile_idx) -> None:
        self.discard_piles[pile_idx].push(self.hand[hand_idx].pop())
