
import sys
import re
import json
import numpy as np

from flatland.envs.rail_env import RailEnv
from flatland.core.grid.rail_env_grid import RailEnvTransitions
from flatland.core.transition_map import GridTransitionMap
from flatland.envs.line_generators import sparse_line_generator
from flatland.envs.rail_env import RailEnv
from flatland.envs.rail_generators import rail_from_grid_transition_map
from flatland.utils.misc import str2bool
from flatland.utils.rendertools import RenderTool
from flatland.envs.observations import GlobalObsForRailEnv

def helper(x):
    return (tuple(x), 0)

def get_env(file):
    f = open(file)
    data = json.load(f)
    f.close()
    
    transitions = RailEnvTransitions()
    rail_map = np.array(data['grid'])
    rail = GridTransitionMap(width=rail_map.shape[1],
                             height=rail_map.shape[0], transitions=transitions)
    rail.grid = rail_map
    city_positions = list(map(tuple,data['start'] + data['target']))
    train_stations = list(map(helper,data['start'] + data['target']))
    city_orientations = [0] * len(city_positions)
    agents_hints = {'city_positions': city_positions,
                    'train_stations': train_stations,
                    'city_orientations': city_orientations
                    }
    optionals = {'agents_hints': agents_hints}
    # make sure correct variation
    check = False
    while(True):
        env = RailEnv(width=rail_map.shape[1],
                  height=rail_map.shape[0],
                  rail_generator=rail_from_grid_transition_map(rail),
                  line_generator=sparse_line_generator(),
                  number_of_agents=len(data['agents']),
                  obs_builder_object=GlobalObsForRailEnv(),
                  )
        for i, agent in enumerate(env.agents):
            if agent.initial_position == data['start'][i]:
                if agent.target == data['target'][i]:
                    if agent.direction == data['direction'][i]:
                        check = True
        if check:
            break
        else:
            continue
    return env


def get_actions(file, n_agents):   
    with open(file, 'r') as f:
        lines = f.readlines()
    f.close()

    # last solution
    for l in lines:
        if l[0] == "a":
            solution = l
            
    # actions
    r1 = re.compile(r'\(\d+,\d+,\d+\)')
    m1 = r1.findall(solution)

    r2 = re.compile(r'\((\d+),(\d+),(\d+)\)')
    actions = [[0] * (len(m1)//n_agents)] * n_agents
    for i in m1:
        m2 = r2.match(i)
        actions[int(m2.group(1))][int(m2.group(3))] = int(m2.group(2))

    return actions

# TDOD finish  
def visualize(env, actions):
    env_renderer = RenderTool(env,
                          #agent_render_variant=AgentRenderVariant.ONE_STEP_BEHIND,
                          show_debug=False,
                          screen_height=600,  # Adjust these parameters to fit your resolution
                          screen_width=800)  # Adjust these parameters to fit your resolution
    
    action_dict = dict()

    # exception -> problem in env
    env.step(action_dict)
    
    # arbitrary number of steps
    for step in range(50):
        # action for each agent in the environment
        for a in range(env.get_num_agents()):
            action_dict.update({a: actions[a][step]})

        # make step
        next_obs, all_rewards, done, _ = env.step(action_dict)

        if env_renderer is not None:
            env_renderer.render_env(show=True, show_observations=False, show_predictions=False)
            env_renderer.gl.save_image('tmp/frames/flatland_frame_{:04d}.png'.format(step))

        print("\n Their current statuses are:")
        print("============================")
        for agent_idx, agent in enumerate(env.agents):
            print("Agent {} status is: {} with its current position being {}".format(
                agent_idx, str(agent.state), str(agent.position)))
            
        if done['__all__']:
            break
        
    # close the renderer / rendering window
    if env_renderer is not None:
        env_renderer.close_window()
    return

def main(argv):
    # TODO check input
    env_file = argv[1]
    asp_file = argv[2]
    
    env = get_env(env_file)
    
    actions = get_actions(asp_file, env.get_num_agents())
    
    # visualize(env, actions)
   
if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv)
    else:
        print("Usage: visualizer.py <env-file.json> <asp-out.txt>")
