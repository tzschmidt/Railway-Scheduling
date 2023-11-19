import getopt
import random
import sys
import time
import os
from typing import Tuple

import numpy as np
import json

from flatland.core.env_observation_builder import DummyObservationBuilder
from flatland.core.grid.rail_env_grid import RailEnvTransitions
from flatland.core.transition_map import GridTransitionMap
from flatland.envs.line_generators import sparse_line_generator
from flatland.envs.rail_env import RailEnv
from flatland.envs.rail_generators import rail_from_grid_transition_map
from flatland.utils.misc import str2bool
from flatland.utils.rendertools import RenderTool
from flatland.envs.observations import GlobalObsForRailEnv


class RandomAgent:

    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size

    def act(self, state):
        """
        :param state: input is the observation of the agent
        :return: returns an action
        """
        return 2  # np.random.choice(np.arange(self.action_size))

    def step(self, memories):
        """
        Step function to improve agent by adjusting policy given the observations

        :param memories: SARS Tuple to be
        :return:
        """
        return

    def save(self, filename):
        # Store the current policy
        return

    def load(self, filename):
        # Load a policy
        return


def custom_rail_map() -> Tuple[GridTransitionMap, np.array]:
    # We instantiate a very simple rail network on a 7x7 grid:
    #   0 1 2 3 4 5 6
    # 0     
    # 1 - - - - - - -    
    # 2     
    # 3
    # 4
    # 5
    # 6

    transitions = RailEnvTransitions()
    cells = transitions.transition_list

    empty = cells[0]
    dead_end_from_south = cells[7]
    right_turn_from_south = cells[8]
    right_turn_from_west = transitions.rotate_transition(right_turn_from_south, 90)
    right_turn_from_north = transitions.rotate_transition(right_turn_from_south, 180)
    right_turn_from_east = transitions.rotate_transition(right_turn_from_south, 270)
    dead_end_from_west = transitions.rotate_transition(dead_end_from_south, 90)
    dead_end_from_north = transitions.rotate_transition(dead_end_from_south, 180)
    dead_end_from_east = transitions.rotate_transition(dead_end_from_south, 270)
    vertical_straight = cells[1]
    simple_switch_north_left = cells[2]
    simple_switch_north_right = cells[10]
    simple_switch_left_east = transitions.rotate_transition(simple_switch_north_left, 90)
    simple_switch_right_east = transitions.rotate_transition(simple_switch_north_right, 90)
    horizontal_straight = transitions.rotate_transition(vertical_straight, 90)
    double_switch_south_horizontal_straight = horizontal_straight + cells[6]
    double_switch_north_horizontal_straight = transitions.rotate_transition(
        double_switch_south_horizontal_straight, 180)
    
    
    # define map
    rail_map = np.array(
        [[right_turn_from_south] + [horizontal_straight] + [right_turn_from_west]+ [empty]+ [right_turn_from_south] + [horizontal_straight] + [right_turn_from_west]] +
        [[vertical_straight] + [empty] + [simple_switch_north_right]+ [horizontal_straight]+ [simple_switch_north_left]+ [empty]+ [vertical_straight]] +
        [[right_turn_from_east] + [simple_switch_right_east]  + [right_turn_from_north]+ [empty]+ [right_turn_from_east] + [simple_switch_right_east]  + [right_turn_from_north]] +
        [[empty] + [vertical_straight]  + [empty]+ [empty]+ [empty]+ [vertical_straight]+ [empty]] +
        [[right_turn_from_south] + [simple_switch_left_east]  + [right_turn_from_west]+ [empty]+ [right_turn_from_south]+ [simple_switch_left_east]  + [right_turn_from_west]] +
        [[vertical_straight] + [empty]  + [simple_switch_north_right]+ [horizontal_straight]+ [simple_switch_north_left] + [empty]+ [vertical_straight]] +
        [[right_turn_from_east] + [horizontal_straight]  + [right_turn_from_north]+ [empty]+ [right_turn_from_east]+ [horizontal_straight]  + [right_turn_from_north]] +
        [[empty] * 7], dtype=np.uint16)
    rail = GridTransitionMap(width=rail_map.shape[1],
                             height=rail_map.shape[0], transitions=transitions)
    rail.grid = rail_map
    city_positions = [(1, 0), (0, 1), (0, 5), (1, 6), (5,0), (6,1), (6,5), (5,6)]
    train_stations = [
        [((1, 0), 0)],
        [((0, 1), 0)],
        [((0, 5), 0)],
        [((1, 6), 0)],
        [((5, 0), 0)],
        [((6, 1), 0)],
        [((6, 5), 0)],
        [((5, 6), 0)]
    ]
    city_orientations = [0, 0, 0, 0, 0, 0, 0, 0]
    agents_hints = {'city_positions': city_positions,
                    'train_stations': train_stations,
                    'city_orientations': city_orientations
                    }
    optionals = {'agents_hints': agents_hints}
    return rail, rail_map, optionals


def create_env():
    rail, rail_map, optionals = custom_rail_map()
    env = RailEnv(width=rail_map.shape[1],
                  height=rail_map.shape[0],
                  rail_generator=rail_from_grid_transition_map(rail, optionals),
                  line_generator=sparse_line_generator(),
                  number_of_agents=4,
                  obs_builder_object=GlobalObsForRailEnv(),
                  )
    return env

def save_as_json(name, env):

    agent_id_list = []
    target = []
    start = []
    agent_dir = []

    for agent_idx, agent in enumerate(env.agents):
        agent_id_list.append(agent_idx)
        target.append(agent.target)
        start.append(agent.initial_position)
        agent_dir.append(agent.direction)

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


def main(args):
    random.seed(100)
    np.random.seed(100)

    env = create_env()
    env.reset()

    # save env as json
    save_as_json("7_7_a_4_test", env)


if __name__ == '__main__':
    if 'argv' in globals():
        main(argv)
    else:
        main(sys.argv[1:])
