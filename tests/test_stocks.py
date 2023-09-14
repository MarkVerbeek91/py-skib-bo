from skip_bo.stocks import GameStock


def test_game_stock_default_number_of_card():
    game_stock = GameStock()
    assert len(game_stock) == 156


def test_game_stock_pop():
    game_stock = GameStock()
    top_cards = game_stock.cards[-1]
    assert game_stock.pop() == top_cards


def test_shuffle_the_game_stock():
    game_stock = GameStock()
    game_stock.shuffle()
    assert game_stock.cards[-5:] != ["X"] * 5


def test_refill_the_game_stock():
    game_stock = GameStock()
    game_stock.refill(["X"])

    assert game_stock.pop() != "X"
