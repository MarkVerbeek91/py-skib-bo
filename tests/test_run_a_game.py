from skip_bo.game_render import display_ascii
from skip_bo.skip_bo import SkipBoGame


def test_run_a_game_for_two():
    main_game = SkipBoGame(number_of_players=2)
    main_game.start()

    for nr in range(5):
        print(f"Round    : {nr:>3}")
        display_ascii(main_game)
        main_game.play_round()
        display_ascii(main_game)
