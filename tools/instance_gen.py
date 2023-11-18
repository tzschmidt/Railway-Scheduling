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
    # We instantiate a very simple rail network on a 3x3 grid:
    #   0 1 2 
    # 0     
    # 1 - - -     
    # 2     
   
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
        [[right_turn_from_south] + [horizontal_straight] + [right_turn_from_west]] +
        [[vertical_straight] + [right_turn_from_south] + [right_turn_from_north]] +
        [[right_turn_from_east] + [simple_switch_left_east]  + [dead_end_from_west]] +
        [[empty] * 3], dtype=np.uint16)
    rail = GridTransitionMap(width=rail_map.shape[1],
                             height=rail_map.shape[0], transitions=transitions)
    rail.grid = rail_map
    city_positions = [(2, 0), (0, 2)]
    train_stations = [
        [((2, 0), 0)],
        [((0, 2), 0)],
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

def save_as_json(name, env):

    agent_id_list = []
    target = []
    start = []

    for agent_idx, agent in enumerate(env.agents):
        agent_id_list.append(agent_idx)
        target.append(agent.target)
        start.append(agent.initial_position)

    grid = env.rail.grid.tolist()
    start_list = start
    target_list = target
    agent = agent_id_list

    data = {
        'grid':grid,
        'agents':agent,
        'target':target_list,
        'start':start_list
    }

    with open("..\instances\{}.json".format(name), "w") as json_file:
        json.dump(data, json_file, indent=4)

def convert_env(name, env):
    
    file = open("..\instances\{}.lp".format(name), "w")
    
    for agent_idx, agent in enumerate(env.agents):
        # agents
        file.write("agent({}).\n".format(agent_idx))
        # start position
        pos = agent.initial_position
        file.write("starting({},({},{})).\n".format(agent_idx, pos[0], pos[1]))
        # direction 
        file.write("direction({},{}).\n".format(agent_idx, agent.direction))
        # target position
        pos = agent.target
        file.write("target({},({},{})).\n".format(agent_idx, pos[0], pos[1]))
    
    # cells and their transitions
    # trans((0,0),1,3) -> cell(0,0) when coming from from east(1) can exit west(3)
    # other appproach trans((0,0),1,0) -> cell(0,0) when facing east(1) can exit north(0)
    grid = env.rail.grid
    for y in range(env.height):
        for x in range(env.width):
            val = "{0:016b}".format(grid[y][x])
            d = [0]*4
            d[2] = val[:4]
            d[3] = val[4:8]
            d[0] = val[8:12]
            d[1] = val[12:]
            # other approach
            #d[0] = val[:4]
            #d[1] = val[4:8]
            #d[2] = val[8:12]
            #d[3] = val[12:]
            cell = False
            for i in range(4):
                c = 0
                for j in range(4):
                    if d[i][j] == '1':
                        file.write("transraw(({},{}),{},{}).\n".format(y, x, i, j))
                        c += 1
                if c != 0:
                    cell = True
                    file.write("trans_count(({},{}),{},{}).\n".format(y, x, i, c))
            if cell:
                file.write("cell({},{}).\n".format(y, x))         
    file.close()
    save_as_json(name, env)
    return
    
def custom_railmap_example(sleep_for_animation, do_rendering):
    random.seed(100)
    np.random.seed(100)

    env = create_env()
    env.reset()

    # convert env to .lp
    convert_env("test", env)    

    # instance gen done ----------------------
    # following code just checks if instance is valid (executable)
    
    if do_rendering:
        env_renderer = RenderTool(env,
                              #agent_render_variant=AgentRenderVariant.ONE_STEP_BEHIND,
                              show_debug=False,
                              screen_height=600,  # Adjust these parameters to fit your resolution
                              screen_width=800)  # Adjust these parameters to fit your resolution

            
    #nv_renderer.render_env(show=True)
    #time.sleep(2)


    controller = RandomAgent(218, 4)


    # check agents
    print("\n Agents in the environment have to solve the following tasks: \n")
    for agent_idx, agent in enumerate(env.agents):
        print(
        "The agent with index {} has the task to go from its initial position {}, facing in the direction {} to its target at {}.".format(
            agent_idx, agent.initial_position, agent.direction, agent.target))

    # check status
    print("\n Their current statuses are:")
    print("============================")
    for agent_idx, agent in enumerate(env.agents):
        print("Agent {} status is: {} with its current position being {}".format(
            agent_idx, str(agent.state), str(agent.position)))

    # Empty dictionary for all agent action
    action_dict = dict()

    # exception -> problem in env
    env.step(action_dict)
    
    # check speed
    print("\n The speed information of the agents are:")
    print("=========================================")
    for agent_idx, agent in enumerate(env.agents):
        print(
        "Agent {} speed is: {:.2f} with the current fractional position being {}/{}".format(
            agent_idx, agent.speed_counter.speed, agent.speed_counter.counter, agent.speed_counter.max_count))

    # check malfunctions
    print("\n The malfunction data of the agents are:")
    print("========================================")
    for agent_idx, agent in enumerate(env.agents):
        print(
        "Agent {} is OK = {}".format(
            agent_idx, agent.malfunction_handler.in_malfunction))


    for a in range(env.get_num_agents()):
        action = controller.act(0)
        action_dict.update({a: action})


    observations, rewards, dones, information = env.step(action_dict)
    print("\n The following agents can register an action:")
    print("========================================")
    for info in information['action_required']:
        print("Agent {} needs to submit an action.".format(info))



    print("\n Start sim:")
    print("========================================")
    if env_renderer is not None:
        env_renderer.reset()

    score = 0
    # Run episode
    frame_step = 0

    os.makedirs("tmp/frames", exist_ok=True)

    for step in range(50):
        # Chose an action for each agent in the environment
        for a in range(env.get_num_agents()):
            action = controller.act(observations[a])
            action_dict.update({a: action})

        # Environment step which returns the observations for all agents, their corresponding
        # reward and whether their are done

        next_obs, all_rewards, done, _ = env.step(action_dict)

        if env_renderer is not None:
            env_renderer.render_env(show=True, show_observations=False, show_predictions=False)
            env_renderer.gl.save_image('tmp/frames/flatland_frame_{:04d}.png'.format(step))

        frame_step += 1
        # Update replay buffer and train agent
        for a in range(env.get_num_agents()):
            controller.step((observations[a], action_dict[a], all_rewards[a], next_obs[a], done[a]))
            score += all_rewards[a]

        print("\n Their current statuses are:")
        print("============================")
        for agent_idx, agent in enumerate(env.agents):
            print("Agent {} status is: {} with its current position being {}".format(
                agent_idx, str(agent.state), str(agent.position)))
            
        observations = next_obs.copy()
        if done['__all__']:
            break
        print('Episode: Steps {}\t Score = {}'.format(step, score))
        
        

    # close the renderer / rendering window
    if env_renderer is not None:
        env_renderer.close_window()



def main(args):
    try:
        opts, args = getopt.getopt(args, "", ["sleep-for-animation=", "do_rendering=", ""])
    except getopt.GetoptError as err:
        print(str(err))  # will print something like "option -a not recognized"
        sys.exit(2)
    sleep_for_animation = True
    do_rendering = True
    for o, a in opts:
        if o in ("--sleep-for-animation"):
            sleep_for_animation = str2bool(a)
        elif o in ("--do_rendering"):
            do_rendering = str2bool(a)
        else:
            assert False, "unhandled option"

    # execute example
    do_rendering = True
    custom_railmap_example(sleep_for_animation, do_rendering)


if __name__ == '__main__':
    if 'argv' in globals():
        main(argv)
    else:
        main(sys.argv[1:])
