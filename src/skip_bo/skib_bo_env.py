import numpy as np
from gymnasium import spaces
from gymnasium.utils import EzPickle

from pettingzoo import AECEnv
from pettingzoo.utils import wrappers
from pettingzoo.utils.agent_selector import agent_selector

from skip_bo.game_render import display_ascii
from skip_bo.skip_bo import SkipBoGame


def env(**kwargs):
    env = raw_env(**kwargs)
    env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


class raw_env(AECEnv, EzPickle):
    metadata = {
        "render_modes": ["ascii"],
        "name": "skib_bo_v1",
        "is_parallelizable": False,
        "render_fps": 2,
    }

    def __init__(self,
                 render_mode: str | None = None,
                 number_of_players: int = 2):
        EzPickle.__init__(self, render_mode)
        super().__init__()

        self.render_mode = render_mode

        self.game = SkipBoGame()

        self.agents = [f"player_{i}" for i in range(number_of_players)]
        self.possible_agents = self.agents[:]

        self.action_spaces = {i: spaces.Discrete(44) for i in self.agents}
        self.observation_spaces = {
            i: spaces.Dict(
                {
                    "observation": spaces.Box(
                        low=0, high=1, shape=(44, 2), dtype=np.int8,
                    ),
                    "action_mask": spaces.Box(
                        low=0, high=1, shape=(44, 2), dtype=np.int8,
                    )
                }
            )
            for i in self.agents
        }

    def observe(self, agent):
        # self.game.


        return {
            "observation": None,
            "action_mask": None
        }

    def observation_space(self, agent):
        return self.observation_spaces[agent]

    def action_space(self, agent):
        return self.action_spaces[agent]

    def _legal_moves(self):
        return []

    def step(self, action):
        ...

    def reset(self, seed=None, options=None):
        # todo more
        self.game = SkipBoGame()
        self.game.start()

        self.agents = self.possible_agents[:]
        self.rewards = {i: 0 for i in self.agents}
        self._cumulative_rewards = {name: 0 for name in self.agents}
        self.terminations = {i: False for i in self.agents}
        self.truncations = {i: False for i in self.agents}
        self.infos = {i: {} for i in self.agents}

        self._agent_selector = agent_selector(self.agents)

        self.agent_selection = self._agent_selector.reset()

    def render(self):
        display_ascii(self.game)

    def check_for_winner(self):
        return self.game.is_game_finished()
