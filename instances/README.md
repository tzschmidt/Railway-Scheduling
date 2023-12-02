# Instances
- `test`:  is our minimal instance with a 2x3 grid and one agent
- `random_test`: is a randomly generated instance with two agents
- `5x5x1-switches`: is a 5x5 intance with one agent and multiple switches to check if a solver doesn't do multiple loops befor going to the target
- `5x5x2-crossing`: is a instance with a crossing in the middle that 2 agents need to pass without colliding
- `5x5x2-switches`: is a 5x5 grid with 2 agents and multiple switches
- `7x7x4-circle`: is a instance with 4 agents on a 7x7 grid that need to move in a circle but could  also stall if the solver doesn't take an optimal path
- `7x7x4-wait`: is the same instance as abovebut this time 2 agents need to wait in order for all agents to reach their target
