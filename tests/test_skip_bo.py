from skip_bo.skip_bo import SkipBoGame, GameStock, BuildPile, Player


def test_create_a_game():
    SkipBoGame()


def test_number_of_cards_in_game_stock():
    assert len(GameStock()) == 156


def test_pop_one_of_game_stock():
    assert len(GameStock().pop()) == 1


def test_pop_many_of_game_stock():
    assert len(GameStock().pop(3)) == 3


def test_shuffle_the_game_stock():
    game_stock = GameStock()
    game_stock.shuffle()
    assert game_stock.pop(3) != ["X"] * 3


def test_push_and_pop_to_build_pile():
    build_pile = BuildPile()
    build_pile.push(1)
    build_pile.push(2)
    assert build_pile.pop() == 2
    assert build_pile.pop() == 1


def test_player_takes_right_amount_from_stock():
    game = SkipBoGame()
    player = Player()
    player.play_round(game)
    assert len(player.cards_in_hand) == 5
