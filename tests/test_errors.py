from skip_bo.erors import IllegalMove


def test_illegal_move_is_exception():
    assert isinstance(IllegalMove(), Exception)
