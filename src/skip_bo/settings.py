import dataclasses


@dataclasses.dataclass
class GameConfigs:
    max_card_value = 12
    nr_hand_cards = 5
    nr_play_field = 4
    nr_discard_piles = 4

    # debug rules
    max_discard_pile_size = 6
