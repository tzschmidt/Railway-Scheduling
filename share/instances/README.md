# Instances
For the 7x7x4 instances a max step limit of 30 is recommended.

- `5x5x1-switches`: is a 5x5 instance with one agent and multiple switches to check if a solver doesn't do multiple loops before going to the target \
  <image src=https://github.com/tzschmidt/Railway-Scheduling/assets/59642899/df181edd-37f5-42a0-b7ed-a41c2fe693e5 width=200 height=200>
- `5x5x2-crossing`: is a instance with a crossing in the middle that 2 agents need to pass without colliding \
  <image src=https://github.com/tzschmidt/Railway-Scheduling/assets/59642899/719c5a8b-a864-49f7-a547-9c6b22623015 width=200 height=200>
- `5x5x2-switches`: is a 5x5 grid with 2 agents and multiple switches \
  <image src=https://github.com/tzschmidt/Railway-Scheduling/assets/59642899/77527dbb-3982-4151-9181-429cc75aa2e0 width=200 height=200>
- `5x5x2-wait`: is a 5x5 grid where one agent is guaranteed to require waiting \
  <image src=https://github.com/tzschmidt/Railway-Scheduling/assets/59642899/c2eb2adf-6e76-4c03-9ca0-89644ff5e734 width=200 height=200>
- `7x7x4-circle`: is a instance with 4 agents on a 7x7 grid that need to move in a circle but could  also stall if the solver doesn't take an optimal path \
  <image src=https://github.com/tzschmidt/Railway-Scheduling/assets/59642899/4bd6f031-6700-4b8a-af3e-b20d17ba951c width=200 height=200>
- `7x7x4-wait`: is the same instance as abovebut this time 2 agents need to wait in order for all agents to reach their target \
  <image src=https://github.com/tzschmidt/Railway-Scheduling/assets/59642899/8fd49fbe-95d0-43da-92c7-7208cb4cc1c0 width=200 height=200>

