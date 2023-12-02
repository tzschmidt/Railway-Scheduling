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
    switch_02_01 = vertical_straight + right_turn_from_east
    switch_02_03 = vertical_straight + right_turn_from_north
    switch_31_12 = horizontal_straight + right_turn_from_south
    switch_31_01 = horizontal_straight + right_turn_from_east
    
    
    # define map
    rail_map = np.array(
        [[right_turn_from_south] + [horizontal_straight] + [right_turn_from_west]+ [empty]+ [right_turn_from_south] + [horizontal_straight] + [right_turn_from_west]] +
        [[vertical_straight] + [empty] + [switch_02_01]+ [horizontal_straight]+ [switch_02_03]+ [empty]+ [vertical_straight]] +
        [[right_turn_from_east] + [simple_switch_right_east]  + [right_turn_from_north]+ [empty]+ [right_turn_from_east] + [switch_31_12]  + [right_turn_from_north]] +
        [[empty] + [vertical_straight]  + [empty]+ [empty]+ [empty]+ [vertical_straight]+ [empty]] +
        [[right_turn_from_south] + [simple_switch_left_east]  + [right_turn_from_west]+ [empty]+ [right_turn_from_south]+ [switch_31_01]  + [right_turn_from_west]] +
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

def set_agent_attributes_circle(env):
    target_position_1 = (6, 1)
    initial_position_1 = (1, 0)
    direction_1 = 0
        
    # Set the target, initial_position, and direction for the first agent
    env.agents[0].target = target_position_1
    env.agents[0].initial_position = initial_position_1
    env.agents[0].direction = direction_1

    target_position_2 = (0, 1)
    initial_position_2 = (1, 6)
    direction_2 = 2
        
    # Set the target, initial_position, and direction for the first agent
    env.agents[1].target = target_position_2
    env.agents[1].initial_position = initial_position_2
    env.agents[1].direction = direction_2

    target_position_3 = (0, 5)
    initial_position_3 = (5, 6)
    direction_3 = 2
        
    # Set the target, initial_position, and direction for the first agent
    env.agents[2].target = target_position_3
    env.agents[2].initial_position = initial_position_3
    env.agents[2].direction = direction_3

    target_position_4 = (6, 5)
    initial_position_4 = (5, 0)
    direction_4 = 0
        
    # Set the target, initial_position, and direction for the first agent
    env.agents[3].target = target_position_4
    env.agents[3].initial_position = initial_position_4
    env.agents[3].direction = direction_4

def set_agent_attributes_wait(env):
    target_position_1 = (6, 5)
    initial_position_1 = (1, 0)
    direction_1 = 0
        
    # Set the target, initial_position, and direction for the first agent
    env.agents[0].target = target_position_1
    env.agents[0].initial_position = initial_position_1
    env.agents[0].direction = direction_1

    target_position_2 = (0, 5)
    initial_position_2 = (1, 6)
    direction_2 = 2
        
    # Set the target, initial_position, and direction for the first agent
    env.agents[1].target = target_position_2
    env.agents[1].initial_position = initial_position_2
    env.agents[1].direction = direction_2

    target_position_3 = (0, 1)
    initial_position_3 = (5, 6)
    direction_3 = 2
        
    # Set the target, initial_position, and direction for the first agent
    env.agents[2].target = target_position_3
    env.agents[2].initial_position = initial_position_3
    env.agents[2].direction = direction_3

    target_position_4 = (6, 1)
    initial_position_4 = (5, 0)
    direction_4 = 0
        
    # Set the target, initial_position, and direction for the first agent
    env.agents[3].target = target_position_4
    env.agents[3].initial_position = initial_position_4
    env.agents[3].direction = direction_4

def create_env():
    rail, rail_map, optionals = custom_rail_map()
    env = RailEnv(width=rail_map.shape[1],
                  height=rail_map.shape[0],
                  rail_generator=rail_from_grid_transition_map(rail, optionals),
                  line_generator=sparse_line_generator(),
                  number_of_agents=4,
                  obs_builder_object=GlobalObsForRailEnv(),
                  )
    env.reset()
    set_agent_attributes_wait(env)
    # set_agent_attributes_circle(env)
    return env

def save_instance(name, env):
    file_path = os.path.join("..", "instances", f"{name}.pkl")
    RailEnvPersister.save(env, file_path)
    return

def main(args):
    random.seed(100)
    np.random.seed(100)

    env = create_env()

    # save env as pkl
    save_instance("7x7y4-wait", env)
    # save_instance("7x7y4-circle", env)


if __name__ == '__main__':
    if 'argv' in globals():
        main(argv)
    else:
        main(sys.argv[1:])
