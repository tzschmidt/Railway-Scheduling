from flatland.envs.rail_env import RailEnv
from flatland.envs.rail_generators import sparse_rail_generator
from flatland.envs.line_generators import sparse_line_generator
from flatland.envs.observations import GlobalObsForRailEnv
import PIL
from flatland.utils.rendertools import RenderTool
from IPython.display import clear_output, display
from flatland.envs.rail_env import RailEnvActions
import numpy as np

class RandomController:
    def __init__(self, action_size):
        self.action_size = action_size

    def act(self, observations):
        actions = dict()
        for agent_handle, observation in enumerate(observations):
            action = np.random.randint(self.action_size)
            actions.update({agent_handle: action})
        return actions


# Render the environment
def render_env(env,wait=True):

    env_renderer = RenderTool(env, gl="PILSVG")
    env_renderer.render_env()

    image = env_renderer.get_image()
    pil_image = PIL.Image.fromarray(image)
    clear_output(wait=True)
    global x
    pil_image.save("./render/test"+str(x)+".png")
    x = x+1


def convert_env(name, env):

    file = open("..\instances\{}.lp".format(name), "w")

    for agent_idx, agent in enumerate(env.agents):
        # agents
        file.write("agent({})\n".format(agent_idx))
        # start position
        pos = agent.initial_position
        file.write("starting({},({},{}))\n".format(agent_idx, pos[0], pos[1]))
        # direction
        file.write("direction({},{})\n".format(agent_idx, agent.direction))
        # target position
        pos = agent.target
        file.write("target({},({},{}))\n".format(agent_idx, pos[0], pos[1]))

    # cells and their transitions
    # trans((0,0),1,3) -> cell(0,0) when coming from from east(1) can exit west(3)
    # other appproach trans((0,0),1,0) -> cell(0,0) when facing east(1) can exit north(0)
    grid = env.rail.grid
    for y in range(env.height):
        for x in range(env.width):
            file.write("cell({},{})\n".format(y, x))
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
            for i in range(4):
                for j in range(4):
                    if d[i][j] == '1':
                        file.write("trans(({},{}),{},{})\n".format(y, x, i, j))

    file.close()


def run_episode(env, controller, observations, info):

    score = 0
    actions = dict()

    for step in range(50):

        actions = controller.act(observations)
        next_observations, all_rewards, dones, info = env.step(actions)
        for agent_handle in env.get_agent_handles():
            score += all_rewards[agent_handle]

        render_env(env)
        print('Timestep {}, total score = {}'.format(step, score))

        if dones['__all__']:
            print('All done!')
            return

    print("Episode didn't finish after 50 timesteps.")


x=0

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

render_env(random_env)

controller = RandomController(random_env.action_space[0])
observations, info = random_env.reset()
actions = controller.act(observations)

# Perform a single action per agent
for (handle, action) in actions.items():
    print('Agent {} will perform action {} ({})'.format(handle, action, RailEnvActions.to_char(action)))
    next_obs, all_rewards, dones, info = random_env.step({handle: action})

print('Rewards for each agent: {}'.format(all_rewards))
print('Done for each agent: {}'.format(dones))
print('Misc info: {}'.format(info))

# run_episode(random_env, controller, observations, info)

convert_env("testing",random_env)