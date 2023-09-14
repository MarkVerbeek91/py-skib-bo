from skip_bo.errors import IllegalMove


def test_illegal_move_is_exception():
    assert isinstance(IllegalMove(), Exception)
