# Railway-Scheduling

## About

This project uses Answer Set Programming (ASP), specifically [clingo](https://potassco.org/clingo/), to solve train scheduling problems. As an framework for instance generation and testing we use [flatland](https://flatland.aicrowd.com/intro.html).

## Directory Structure
- `./all_instances/` contains all instances used for testing
- `./encodings/` contains all ASP related files used for the scheduling
- `./instances/` contains all custom instances
- `./share/` contains all instances and encodings provided for other groups
- `./testing/` contains all testing results and plots
- `./tools/` contains all tools and scripts, e.g. for instance generation

## ASP representation of the scenario
### Grid
- cells in the grid are represented as `cell(Y,X))`
- directions are represented as numbers 0-3 (0=north, 1=east, 2=south and 3=west of the cell)
- transitions are represented as `transraw((Y,X),IN,OUT)` with `IN` and `OUT` being the directions from which a cell can be entered and then left
- number of transitions `C` per cell `(Y,X)` per entry direction `D` are represented as `trans_count((Y,X),D,C)` 
### Agents
all agents have:
- an ID (starting with 0), written as `agent(ID)`
- a starting location `starting(ID,(Y,X))`
- a direction in which they start, written as `direction(ID,DIRECTION)`
- a target/goal written as `target(ID,(Y,X))`
### Example 
#### Simple instance example 
`agent(0).`\
`starting(0,(1,0)).`\
`direction(0,2).`\
`target(0,(0,2)).`\
`transraw((0,0),1,2).`\
`transraw((0,0),2,1).`\
`cell((0,0),2).`\
`transraw((0,1),1,3).`\
`transraw((0,1),3,1).`\
`cell((0,1),2).`\
`transraw((0,2),2,3).`\
`transraw((0,2),3,2).`\
`cell((0,2),2).`\
`transraw((1,0),0,1).`\
`transraw((1,0),1,0).`\
`cell((1,0),2).`\
`transraw((1,1),1,3).`\
`transraw((1,1),3,1).`\
`cell((1,1),2).`\
`transraw((1,2),0,3).`\
`transraw((1,2),3,0).`\
`cell((1,2),2).`

which represents the following scenario:

![flatland_frame_0000](https://github.com/tzschmidt/Railway-Scheduling/assets/59642899/016a17ec-dd42-433a-90e9-53aba14cd13b)


