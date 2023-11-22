
import sys
import re
import time
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
    r1 = re.compile(r'\(\d+,\d+,\d+\)')
    m1 = r1.findall(solution)

    r2 = re.compile(r'\((\d+),(\d+),(\d+)\)')
    actions = [[0] * (len(m1)//n_agents)] * n_agents
    for i in m1:
        m2 = r2.match(i)
        actions[int(m2.group(1))][int(m2.group(3))] = int(m2.group(2))

    return actions

    
# TODO finish  
def visualize(env, actions, max_steps: int = 50, sim_delay: float = 0.5):
    env_renderer = RenderTool(env,
                          #agent_render_variant=AgentRenderVariant.ONE_STEP_BEHIND,
                          show_debug=False,
                          screen_height=600,  # Adjust these parameters to fit your resolution
                          screen_width=800)  # Adjust these parameters to fit your resolution
    
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
                        actions_dict[agent.handle] = RailEnvActions.MOVE_FORWARD

                    if idx in agents_step:
                        print(
                            f"Agent({idx}) is at {agent.position} and chose {Action(actionsdict[agent.handle])} at step {agents_step[idx]}/{len(self.agent_actions[idx])-1}.")
                    else:
                        print(
                            f"Agent({idx}) not spawned yet. {agent.state}")

                env.step(actions_dict)

                env_renderer.render_env(show=True,
                                             return_image=True, show_rowcols=True, show_predictions=True, step=0)

                time.sleep(sim_delay)
                step += 1
    except Exception as e:
        print(
            f"An exception occured which would otherwise have closed the rendering window.\n\n{e}\n")
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
