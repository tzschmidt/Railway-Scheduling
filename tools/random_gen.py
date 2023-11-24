from flatland.envs.rail_env import RailEnv
from flatland.envs.rail_generators import sparse_rail_generator
from flatland.envs.line_generators import sparse_line_generator
from flatland.envs.observations import GlobalObsForRailEnv
import PIL
from flatland.utils.rendertools import RenderTool
from IPython.display import clear_output, display
from flatland.envs.rail_env import RailEnvActions
import numpy as np
from flatland.envs.persistence import RailEnvPersister


def save_instance(name, env):

    RailEnvPersister.save(env, "..\instances\{}.pkl".format(name))
    return

def create_env():

    rail_generator = sparse_rail_generator(
        max_num_cities=2,
        grid_mode=False,
        max_rails_between_cities=2,
        max_rail_pairs_in_city=2
    )

    # Initialize the properties of the environment
    random_env = RailEnv(
        width=24,
        height=24,
        number_of_agents=1,
        rail_generator=rail_generator,
        line_generator=sparse_line_generator(),
        obs_builder_object=GlobalObsForRailEnv()
    )
    return random_env

def main():
    env = create_env()
    env.reset()
    save_instance("random_test", env)

if __name__ == '__main__':
        main()