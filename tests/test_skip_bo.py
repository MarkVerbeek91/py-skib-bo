import numpy as np
import pytest

from skip_bo.skip_bo import SkipBoGame, GameStock, BuildPile, Player, IllegalMove


def test_create_a_game():
    SkipBoGame()


def test_number_of_cards_in_game_stock():
    assert len(GameStock()) == 156


def test_pop_one_of_game_stock():
    assert len(GameStock().pop()) == 1


def test_build_pile_had_right_properties():
    build_pile = BuildPile()
    assert build_pile.top_card == 0
    assert build_pile.accepts == 1

    build_pile.push("X")
    assert build_pile.top_card == 1
    assert build_pile.accepts == 2

    build_pile.push(2)
    assert build_pile.top_card == 2
    assert build_pile.accepts == 3

    build_pile.push("X")
    assert build_pile.top_card == 3
    assert build_pile.accepts == 4

    build_pile.push("X")
    assert build_pile.top_card == 4
    assert build_pile.accepts == 5

    with pytest.raises(IllegalMove):
        build_pile.push(12)


def test_shuffle_the_game_stock():
    game_stock = GameStock()
    game_stock.shuffle()
    assert game_stock.pop() != "X"


def test_push_and_pop_to_build_pile():
    build_pile = BuildPile()
    build_pile.push(1)
    build_pile.push(2)
    assert build_pile.pop() == 2
    assert build_pile.pop() == 1


def test_player_accepts_just_enough_cards():
    player = Player()
    [player.deal_hand_card("X") for _ in range(5)]

    with pytest.raises(IllegalMove):
        player.deal_hand_card(1)


def test_build_pile_shows_correct_data():
    build_pile = BuildPile()
    assert build_pile.top_card == 0
    assert build_pile.accepts == 1


def test_legal_moves():
    game = SkipBoGame(number_of_players=2)
    game.start()

    player = game.players[0]

    assert sum(game.legal_moves(player)) == 20


def test_legal_moves_for_set_up_field():
    game = SkipBoGame(number_of_players=2)
    player_01 = Player()
    player_02 = Player()

    game.players = [player_01, player_02]

    player_01.deal_stock_card(3)
    player_02.deal_stock_card(3)

    player_01.deal_hand_card(1)
    map(player_01.deal_hand_card, [12] * 4)

    player_02.deal_hand_card(2)
    map(player_02.deal_hand_card, [12] * 4)

    player = game.players[0]

    assert sum(game.legal_moves(player)) == 24


def test_legal_moves_for_set_up_field_02():
    game = SkipBoGame(number_of_players=2)
    player_01 = Player()
    player_02 = Player()

    game.players = [player_01, player_02]

    player_01.deal_stock_card("X")
    player_02.deal_stock_card(3)

    player_01.deal_hand_card(1)
    map(player_01.deal_hand_card, [12] * 4)

    player_02.deal_hand_card(2)
    map(player_02.deal_hand_card, [12] * 4)

    player = game.players[0]

    assert sum(game.legal_moves(player)) == 28


@pytest.mark.parametrize(
    "action_id",
    range(4)
)
def test_game_makes_step_by_player_plays_stock_card(action_id):
    game = SkipBoGame(number_of_players=2)
    player_01 = Player()

    game.players = [player_01]

    player_01.deal_stock_card(1)

    player_id = 0
    game.step(player_id, action_id)

    expected_result = [0 if i != action_id else 1 for i in range(4)]
    assert game.field_cards == expected_result


@pytest.mark.parametrize(
    "action_id",
    list(range(4, 4 + 20))
)
def test_game_makes_step_by_player_plays_hand_card(action_id):
    game = SkipBoGame(number_of_players=2)
    player_01 = Player()

    game.players = [player_01]

    list(map(player_01.deal_hand_card, [1] * 5))

    player_id = 0
    game.step(player_id, action_id)

    expected_result = [0 if i != (action_id % 4) else 1 for i in range(4)]
    assert game.field_cards == expected_result


@pytest.mark.parametrize(
    "action_id",
    list(range(4 + 20, 4 + 20 + 20))
)
def test_game_makes_step_by_player_discards_card(action_id):
    game = SkipBoGame(number_of_players=2)
    player_01 = Player()

    game.players = [player_01]

    list(map(player_01.deal_hand_card, [1] * 5))

    player_id = 0
    game.step(player_id, action_id)

    expected_result = [0 if i != (action_id % 4) else 1 for i in range(4)]
    assert player_01.discard_cards == expected_result
