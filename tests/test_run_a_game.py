import time

import pettingzoo

from sb3_contrib import MaskablePPO
from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from sb3_contrib.common.wrappers import ActionMasker

from skip_bo.game_render import display_ascii
from skip_bo.skip_bo import SkipBoGame

from skip_bo.skib_bo_env import env as env_fn


def test_run_a_game_for_two():
    main_game = SkipBoGame(number_of_players=2)
    main_game.start()

    for nr in range(5):
        print(f"Round    : {nr:>3}")
        display_ascii(main_game)
        main_game.play_round()
        display_ascii(main_game)


class SB3ActionMaskWrapper(pettingzoo.utils.BaseWrapper):

    def reset(self, seed=None, options=None):
        super().reset(seed, options)

        self.observation_space = super().observation_space(self.possible_agents[0])["observation"]
        self.action_space = super().action_space(self.possible_agents[0])

        # Return initial observation, info (PettingZoo AEC envs do not by default)
        return self.observe(self.agent_selection), {}

    def step(self, action):
        super().step(action)
        return super().last()

    def observe(self, agent):
        return super().observe(agent)["observation"]

    def action_mask(self):
        return super().observe(self.agent_selection)["action_mask"]


def mask_fn(env):
    # Do whatever you'd like in this function to return the action mask
    # for the current env. In this example, we assume the env has a
    # helpful method we can rely on.
    return env.action_mask()


def test_train_the_agents():
    env_kwargs = {}
    env = env_fn(**env_kwargs)

    print(f"Starting training on {str(env.metadata['name'])}.")

    # Custom wrapper to convert PettingZoo envs to work with SB3 action masking
    env = SB3ActionMaskWrapper(env)

    env.reset(seed=0)  # Must call reset() in order to re-define the spaces

    env = ActionMasker(env, mask_fn)

    model = MaskablePPO(MaskableActorCriticPolicy, env, verbose=1)
    model.set_random_seed(0)
    model.learn(total_timesteps=10_000)

    model.save(f"{env.unwrapped.metadata.get('name')}_{time.strftime('%Y%m%d-%H%M%S')}")

    print("Model has been saved.")

    print(f"Finished training on {str(env.unwrapped.metadata['name'])}.\n")

    env.close()
