
import sys
from flatland.envs.rail_env import RailEnv
from flatland.envs.persistence import RailEnvPersister

def load_instance(file):
    
    env, env_dict = RailEnvPersister.load_new(file)
    return env

def convert_env(file, env):

    file = open(file, "w")

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
    grid = env.rail.grid
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            val = "{0:016b}".format(grid[y][x])
            d = [0]*4
            d[2] = val[:4]
            d[3] = val[4:8]
            d[0] = val[8:12]
            d[1] = val[12:]
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
    return

def main(argv):
    # TODO check input
    env_file = argv[1]
    asp_file = argv[2]
    
    env = load_instance(env_file)
    
    convert_env(asp_file, env)
    
   
if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv)
    else:
        print("Usage: pkl_to_lp.py <env-file.pkl> <env-file.lp>")

