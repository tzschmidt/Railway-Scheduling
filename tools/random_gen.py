from flatland.envs.rail_env import RailEnv
from flatland.envs.rail_generators import sparse_rail_generator
from flatland.envs.line_generators import sparse_line_generator
from flatland.envs.observations import GlobalObsForRailEnv
import PIL
from flatland.utils.rendertools import RenderTool
from IPython.display import clear_output, display
from flatland.envs.rail_env import RailEnvActions
import numpy as np
import json

class RandomController:
    def __init__(self, action_size):
        self.action_size = action_size

    def act(self, observations):
        actions = dict()
        for agent_handle, observation in enumerate(observations):
            action = np.random.randint(self.action_size)
            actions.update({agent_handle: action})
        return actions


def save_as_json(name, env):

    agent_id_list = []
    target = []
    start = []
    agent_dir = []

    for agent_idx, agent in enumerate(env.agents):
        agent_id_list.append(agent_idx)
        target.append([int(x) for x in agent.target])
        start.append([int(y) for y in agent.initial_position])
        agent_dir.append(agent.direction.tolist())

    grid = env.rail.grid.tolist()
    start_list = start
    target_list = target
    agent = agent_id_list
    agent_direction = agent_dir

    data = {
        'grid':grid,
        'agents':agent,
        'target':target_list,
        'start':start_list,
        'agent_direction':agent_direction
    }

    with open("..\instances\{}.json".format(name), "w") as json_file:
        json.dump(data, json_file, indent=4)

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

    # Call reset() to initialize the environment
    observation, info = random_env.reset()

    controller = RandomController(random_env.action_space[0])
    observations, info = random_env.reset()
    actions = controller.act(observations)

    # Perform a single action per agent
    for (handle, action) in actions.items():
        next_obs, all_rewards, dones, info = random_env.step({handle: action})


def main(args):
    create_env()
    save_as_json("random_test",random_env)
