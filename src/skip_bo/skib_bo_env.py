

from gymnasium.spaces import Discrete


def env(render_mode=None):
    ...


def raw_env():
    ...



class ActionMask:
    def __init__(self, game):
        self._game = game

    def legal_moves(self):
        return []


def get_action_space(game, player):
    # possible moves:
    # top card from stock to one of the fields (4 moves)
    # each card from hand to one of the field (5*4 moves)
    # each card from hand to one of the discard piles (5*4 moves)
    actions = {

    }


class ObservationSpace:
    def __init__(self):
        pass

    def space(self):
        # possible observations
        # 0. top card to player stock
        # 1. all cards in the hand of player
        # 2. all top cards of play field
        # 3. top (3) cards of player own discard pile
        # 3b. top (3) cards of opponent discard pile (advanced, player number dependent)
        return self.hand_cards_to_field(range(4), range(5)),

    @staticmethod
    def hand_cards_to_field(h_idx, f_idx) -> list:
        return list(map(lambda x: (x[0], x[1]), itertools.product(h_idx, f_idx)))
