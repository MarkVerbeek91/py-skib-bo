import itertools

import pytest

from skip_bo.skip_bo import Player, SkipBoGame


@pytest.fixture
def player():
    return Player("Alice")


def test_player_shows_its_name(player):
    assert str(player) == "Player Alice"


def test_player_get_stock_card_dealt(player):
    player.deal_stock_card(1)

    assert player.stock_card == 1


def test_player_get_hand_card_dealt(player):
    player.deal_hand_card(3)
    assert player.hand_cards == [3] + [0] * 4


def test_player_is_finished(player):
    assert player.is_finished()


@pytest.mark.parametrize(
    "field_idx",
    list(range(4))
)
def test_player_plays_stock_card(player, field_idx):
    player.deal_stock_card(2)
    player.deal_stock_card(1)

    game = SkipBoGame()

    player.play_stock_card(game, field_idx)

    assert player.stock_card == 2
    assert game.play_fields[field_idx].top_card == 1


@pytest.mark.parametrize(
    "hand_idx, field_idx",
    itertools.product(range(5), range(4)),
)
def test_player_discard_card(player, hand_idx, field_idx):
    list(map(player.deal_hand_card, [3] * 5))

    player.discard_card(hand_idx, field_idx)

    expected_result = [3 if i != hand_idx else 0 for i in range(5)]
    assert player.hand_cards == expected_result
    assert player.discard_piles[field_idx].top_card == 3


@pytest.mark.parametrize(
    "hand_idx, field_idx",
    itertools.product(range(5), range(4)),
)
def test_player_plays_hand_card(player, hand_idx, field_idx):
    list(map(player.deal_hand_card, [1] * 5))

    game = SkipBoGame()

    player.play_hand_card(game, hand_idx, field_idx)

    expected_result = [1 if i != hand_idx else 0 for i in range(5)]
    assert player.hand_cards == expected_result
    assert game.play_fields[field_idx].top_card == 1
