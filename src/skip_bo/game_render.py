def display_ascii(game):
    for player in game.players:
        print_player_status(player)

    h = " ".join([f"[{str(x):>2}]" for x in game.play_fields])
    print(f"field    : {h}")
    print("")


def print_player_status(player):
    name = player.name

    h = " ".join([f"[{str(x):>2}]" for x in player.hand])
    print(f"player {name} : {h}")
    h = player.discard_piles
    h = " ".join([f"[{str(x):>2}]" for x in h])
    s = player.stock.top_card
    print(f"         : {h}      [{str(s):>2}]")
