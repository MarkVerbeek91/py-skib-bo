"""Ways to render the game state to the user."""


def display_ascii(game):
    """Display the game state as ascii art."""
    for player in game.players:
        print_player_status(player)

    h = " ".join([f"[{str(x):>2}]" for x in game.play_fields])
    print(f"field    : {h}\n")


def print_player_status(player):
    """Print the status of a player."""
    name = player.name

    h = " ".join([f"[{str(x):>2}]" for x in player.hand])
    print(f"player {name} : {h}")
    h = player.discard_piles
    h = " ".join([f"[{str(x):>2}]" for x in h])
    s = player.stock.top_card
    print(f"         : {h}      [{str(s):>2}]")
