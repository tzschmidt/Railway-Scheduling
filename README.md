# Railway-Scheduling

## About

This project uses Anser Set Programming (ASP), specifically [clingo](https://potassco.org/clingo/), to solve train scheduling problems. As an framework for instance generation and testing we use [flatland](https://flatland.aicrowd.com/intro.html).

## Directory Structure
- './encodinds/' contains all ASP related files used for the scheduling
- './instances/' contains all instances used for testing
- './tools/' contains all tools and scripts, e.g. for instance generation

## ASP encoding
### Grid
- cells in the grid are represented as cell((Y,X),c) where c is the number of connections
- directons are represented as numbers 0-3 (0=north, 1=east, 2=south and 3=west of the cell)
- transitions are represented as transraw((Y,X),IN,OUT) whith IN and OUT being the directions from which a cell can be passed 
### Agents
all agents have:
- an ID (starting with 0), written as agent(ID)
- a starting location starting(ID,(Y,X))
- a direction in wich they start, written as direction(ID,DIRECTION)
- a target/goael written as target(ID,(Y,X))
### Example 
#### Simple code example 
agent(0).\
starting(0,(1,0)).\
direction(0,2).\
target(0,(0,2)).\
transraw((0,0),1,2).\
transraw((0,0),2,1).\
cell((0,0),2).\
transraw((0,1),1,3).\
transraw((0,1),3,1).\
cell((0,1),2).\
transraw((0,2),2,3).\
transraw((0,2),3,2).\
cell((0,2),2).\
transraw((1,0),0,1).\
transraw((1,0),1,0).\
cell((1,0),2).\
transraw((1,1),1,3).\
transraw((1,1),3,1).\
cell((1,1),2).\
transraw((1,2),0,3).\
transraw((1,2),3,0).\
cell((1,2),2).

which looks like this:

![flatland_frame_0000](https://github.com/tzschmidt/Railway-Scheduling/assets/59642899/016a17ec-dd42-433a-90e9-53aba14cd13b)


