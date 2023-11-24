import getopt
import random
import sys
import time
import os
from typing import Tuple

import numpy as np

from flatland.core.env_observation_builder import DummyObservationBuilder
from flatland.core.grid.rail_env_grid import RailEnvTransitions
from flatland.core.transition_map import GridTransitionMap
from flatland.envs.line_generators import sparse_line_generator
from flatland.envs.rail_env import RailEnv
from flatland.envs.rail_generators import rail_from_grid_transition_map
from flatland.utils.misc import str2bool
from flatland.utils.rendertools import RenderTool
from flatland.envs.observations import GlobalObsForRailEnv
from flatland.envs.persistence import RailEnvPersister


def custom_rail_map() -> Tuple[GridTransitionMap, np.array]:
    # We instantiate a very simple rail network on a 5x5 grid:
    #   0 1 2 3 4
    # 0     
    # 1 - - - - -    
    # 2     
    # 3
    # 4

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
    horizontal_straight = transitions.rotate_transition(vertical_straight, 90)
    double_switch_south_horizontal_straight = horizontal_straight + cells[6]
    double_switch_north_horizontal_straight = transitions.rotate_transition(
        double_switch_south_horizontal_straight, 180)
    
    
    # define map
    rail_map = np.array(
        [[right_turn_from_south] + [right_turn_from_west] + [empty]+ [right_turn_from_south]+ [right_turn_from_west]] +
        [[vertical_straight] + [simple_switch_north_right] + [horizontal_straight]+ [simple_switch_north_left]+ [vertical_straight]] +
        [[right_turn_from_east] + [right_turn_from_north]  + [empty]+ [vertical_straight]+ [vertical_straight]] +
        [[right_turn_from_south] + [horizontal_straight]  + [horizontal_straight]+ [right_turn_from_north]+ [vertical_straight]] +
        [[right_turn_from_east] + [horizontal_straight]  + [horizontal_straight]+ [horizontal_straight]+ [right_turn_from_north]] +
        [[empty] * 5], dtype=np.uint16)
    rail = GridTransitionMap(width=rail_map.shape[1],
                             height=rail_map.shape[0], transitions=transitions)
    rail.grid = rail_map
    city_positions = [(1, 0), (1, 4)]
    train_stations = [
        [((1, 0), 0)],
        [((1, 4), 0)],
    ]
    city_orientations = [0, 0]
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
                  number_of_agents=1,
                  obs_builder_object=GlobalObsForRailEnv(),
                  )
    return env

def save_instance(name, env):

    RailEnvPersister.save(env, "..\instances\{}.pkl".format(name))
    return
    

def main(args):
    random.seed(100)
    np.random.seed(100)

    env = create_env()
    env.reset()

    # save env as pkl
    save_instance("5_5_a_1", env)

if __name__ == '__main__':
    if 'argv' in globals():
        main(argv)
    else:
        main(sys.argv[1:])
