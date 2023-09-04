import pytest

from skip_bo.skip_bo import SkipBoGame, GameStock, BuildPile, Player, ObservationSpace, IllegalMove


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
    assert player.number_of_hand_cards == 0

    [player.deal_hand_card(1) for _ in range(3)]
    assert player.number_of_hand_cards == 3

    [player.deal_hand_card(1) for _ in range(2)]
    assert player.number_of_hand_cards == 5

    with pytest.raises(IllegalMove):
        player.deal_hand_card(1)


def test_build_pile_shows_correct_data():
    build_pile = BuildPile()
    assert build_pile.top_card == 0
    assert build_pile.accepts == 1

# def test_observation_space():
#     observation_space = ObservationSpace()
#     assert observation_space.space() == []
