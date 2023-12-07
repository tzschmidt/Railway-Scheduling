
import sys
import re
import time
import os
import msvcrt
import numpy as np

from flatland.envs.rail_env import RailEnv, RailEnvActions
from flatland.core.grid.rail_env_grid import RailEnvTransitions
from flatland.core.transition_map import GridTransitionMap
from flatland.envs.line_generators import sparse_line_generator
from flatland.envs.rail_env import RailEnv
from flatland.envs.rail_generators import rail_from_grid_transition_map
from flatland.utils.misc import str2bool
from flatland.utils.rendertools import RenderTool
from flatland.envs.observations import GlobalObsForRailEnv
from flatland.envs.persistence import RailEnvPersister


def load_env(file):
    env, env_dict = RailEnvPersister.load_new(file)
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
    # TODO use only one regex
    actions = [[]] * n_agents
    for i in range(n_agents):
        m1 = re.findall(rf'\({i},\d+,\d+\)', solution)
        actions[i] = [0] * len(m1)
        for j in m1:
            m2 = re.match(rf'\({i},(\d+),(\d+)\)', j)
            actions[i][int(m2.group(2))] = int(m2.group(1))
    
    return actions

    
def visualize(env, actions, max_steps: int = 50, sim_delay: float = 0.5):
    
    # clear frames
    frames_folder = 'tmp/frames'
    for f in os.listdir(frames_folder):
        fp = os.path.join(frames_folder, f)
        if os.path.isfile(fp):
            os.remove(fp)
    
    env_renderer = RenderTool(env,
                          #agent_render_variant=AgentRenderVariant.ONE_STEP_BEHIND,
                          show_debug=False,
                          screen_height=600,  # Adjust these parameters to fit your resolution
                          screen_width=800)  # Adjust these parameters to fit your resolution
    env.reset()
    # run env
    # based on https://github.com/fbiannis/flatland-asp-collab/blob/main/flatlandasp/flatland_asp.py
    try:
            step = 0
            agents_step = {}
            for id in range(len(actions)):
                print(f"Agent {id} action count {len(actions[id])}")
            while not env.dones["__all__"] and step < max_steps:
                actions_dict = {}
                print(f"Actions for step: {step}")
                for idx, agent in enumerate(env.agents):
                    if agent.position:
                        if not env.dones[idx]:
                            if idx in agents_step:
                                agents_step[idx] += 1
                            else:
                                agents_step[idx] = 0
                            actions_dict[agent.handle] = actions[idx][agents_step[idx]]
                    else:
                        actions_dict[agent.handle] = 2

                    if idx in agents_step:
                        print(
                            f"Agent({idx}) is at {agent.position} and chose {actions_dict[agent.handle]} at step {agents_step[idx]}/{len(actions[idx])-1}.")
                    else:
                        print(
                            f"Agent({idx}) not spawned yet. {agent.state}")

                env.step(actions_dict)

                env_renderer.render_env(show=True,
                                             return_image=True, show_rowcols=True, show_predictions=True, step=0)
                env_renderer.gl.save_image('tmp/frames/flatland_frame_{:04d}.png'.format(step))
                time.sleep(sim_delay)
                step += 1
    except Exception as e:
        print(
            f"An exception occured which would otherwise have closed the rendering window.\n\n{e}\n")
        
    print('\nDone: frames can be found in \'tmp/frames/\'')
    
    if env_renderer is not None:
        env_renderer.close_window()
        
    return

def main(argv):
    # TODO check input
    env_file = argv[1]
    asp_file = argv[2]
    
    env = load_env(env_file)
    
    actions = get_actions(asp_file, env.get_num_agents())
    
    visualize(env, actions)
   
if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv)
    else:
        print("Usage: visualizer.py <env-file.pkl> <asp-out.txt>")
