# Encodings

## Usage
`clingo helper.lp <scheduler>.lp ../instances/<instance>.lp [-c slimit=<step-limit>]`
If there is no step limit given, a limit of 10 will be used. This is subject to change.

## helper.lp
The `helper.lp` encoding provides some general utilities, which can be used in different encodings and approaches.
```
% directions
% north
conv(0,(-1,0)).
% east
conv(1,(0,1)).
% south
conv(2,(1,0)).
% west
conv(3,(0,-1)).
```
The `conv(DIR,(DY,DX))` facts above provide an easy way to convert a direction `DIR` into relative coordinates `(DY,DX)`, e.g. 0 (north) -> (-1,0) (origin of coordinates is at the top-left).

```
% transitions
trans((Y+DY1,X+DX1),(Y,X),(Y+DY2,X+DX2)) :- transraw((Y,X),D1,D2), conv(D1,(DY1, DX1)), conv(D2,(DY2,DX2)).
```
The instances provide facts in the form of `transraw((Y,X),IN,OUT)`, which states, that cell `(Y,X)` can be exited in direction `OUT` when previously entered from direction `IN`. `trans(C1,C2,C3)` contains the same information just applied to a triple of cells instead of using directions. This allows for a mostly position-based approach.

```
% turns:
turn(-1,1).
turn(1,1).
turn(1,-1).
turn(-1,-1).
```
To later address all possible turns, the relative position changes are defined here using `turn(DY,DX)`. 

## scheduler.lp
`scheduler.lp` implements a position-based approach to solving flatland instances.
```
% step limit
#const slimit=20.

step(1..slimit).
```
The maximum number of steps is defined via the `slimit` constant (default = 20). Using `slimit` `step(S)` are generated to represent the different time steps.

```
% start positions
at(A,(Y,X),0) :- agent(A), starting(A,(Y,X)).

% generate positions
0{at(A,(Y,X),S) : cell(Y,X)}1 :- agent(A), step(S).
```
The lines above show the generation of position for each agent. To keep track of the positions the atom `at(A,(Y,X),S)` is used. Meaning agent `A` is at cell `(Y,X)` at step `S`. First, the positions at step 0 are copied from the starting positions given by the instance.    
Secondly for each agent and step at least one cell is assigned. This assignment is very open and thus results in a large search tree for the solver. Hence this line will be our focus for future improvements for example by limiting the available cells for assignment to neighbouring cells.

```
% finish at target
:- not at(A,(Y,X),_), target(A,(Y,X)), agent(A).
% dont move away from target
:- at(A,C,S1), at(A,_,S2), S1<S2, target(A,C), agent(A).
```
To make sure the agents achieve their objective two constraints are introduced. While the first constraint guarantees, that agents finish at their target, the second one prohibits agents from occupying any position once they reached their target. The latter is based on the property of flatland, that agents can despawn once their target is reached. Should this not be the case the last constraint should be removed to allow the encoding to solve specific corner cases.

```
% no collisions
% vertex
:- at(A1,(Y,X),S), at(A2,(Y,X),S), step(S), agent(A1), agent(A2), A1!=A2.
% edge
:- at(A1,(Y1,X1),S), at(A2,(Y2,X2),S), at(A1,(Y2,X2),S-1), at(A2,(Y1,X1),S-1),
	step(S), agent(A1), agent(A2), A1!=A2.
```
In a flatland scenario, two types of collisions can occur. Vertex collisions (two agents at the same position at the same step) and edge collisions (two agents collide while swapping positions). The constraints above prohibit both collision types.

```
% keep track of orientation via cell which agent entered from
% starting direction
entered_from(A,(Y-DY,X-DX),0) :- starting(A,(Y,X)), direction(A,D), conv(D,(DY,DX)), trans((Y-DY,X-DX),(Y,X),_).
% dead-end
entered_from(A,(Y+DY,X+DX),0) :- starting(A,(Y,X)), direction(A,D), conv(D,(DY,DX)), not trans((Y-DY,X-DX),(Y,X),_).
% wait
entered_from(A,(Y1,X1),S) :- at(A,(Y,X),S), at(A,(Y,X),S-1), entered_from(A,(Y1,X1),S-1), agent(A), step(S).
% move
entered_from(A,C,S) :- at(A,C1,S), at(A,C,S-1), C!=C1, agent(A), step(S).
```
The movement of all agents is constrained by the train track layout of the instance, i.e. its transitions. Since all valid transitions are denoted as cell triples `trans(C1,C2,C3)` as stated above in the helper.lp section, this approach causes problems when agents are waiting. To fix this `entered_from(A,C,S)` are introduced. These keep track of the previous (different) cell `C` for each agent `A` at each time step `S`.

```
% only valid actions
% move to neighbors or wait
:- at(A,(Y1,X1),S-1), at(A,(Y2,X2),S), |Y1-Y2|+|X1-X2|>1, step(S), agent(A). 
% continuous
:- not at(A,_,S-1), at(A,_,S), step(S), agent(A).
% transitions
:- entered_from(A,C1,S-1), at(A,C2,S-1), at(A,C3,S), C2!=C3, not trans(C1,C2,C3), step(S), agent(A).
```
All remaining criteria for a valid path are the constraints above. First, all disconnected paths are removed, i.e. positions for each agent at each time step represented by `at(A,C,S)` have to be either adjacent or the same as the previous step.   
Secondly, the path should be continuous, so all paths where positions for steps in between are missing are removed.    
The last constraint checks, that all paths respect the given transitions. Since this encoding was developed incrementally some constraints might be unneeded and could be removed with further testing.

```
% actions:
% none: 0
% left: 1
action(A,1,S) :- entered_from(A,(Y,X-DX),S), at(A,(Y,X),S), at(A,(Y+DY,X),S+1), turn(DY,DX), DY+DX=0, trans_count((Y,X),D,N), conv(D,(0,-DX)), N>=2.
action(A,1,S) :- entered_from(A,(Y-DY,X),S), at(A,(Y,X),S), at(A,(Y,X+DX),S+1), turn(DY,DX), DY+DX!=0, trans_count((Y,X),D,N), conv(D,(-DY,0)), N>=2.
```
To transform the valid solution back into flatland interpretable actions, `action(A,AC,S)` is introduced (agent `A` performs action `AC` at step `S`). Since the "none" action is unused in our solution it can be ignored.    
The left turn with action number 1 is shown above. A turn equals a change in position by the values represented in `turn(DY,DX)` in two steps (one on the x-axis and one on the y-axis). Does the sum of `DY` and `DX` equal 0, the first step has to be done along the x-axis (for a left turn).   
Similarly for a sum other than 0 the first step has to be taken along the y-axis.    
To avoid "false" left turns (track goes left, but no switch), `trans_count(C,D,N)` keeps track of the number of transitions `N` per cell `C` for each direction `D` the agent could enter from. If this value is equal to or bigger than 2, the cell contains a switch.    
Using this, all left turns and therefore necessary "left" actions can be found by checking the positions of each agent at all steps.

```
% forward: 2
action(A,2,S) :- entered_from(A,(Y+DY,X+DX),S), at(A,(Y,X),S), at(A,(Y1,X1),S+1), Y!=Y1, trans_count((Y,X),D,N), conv(D,(DY,DX)), N=1.
action(A,2,S) :- entered_from(A,(Y+DY,X+DX),S), at(A,(Y,X),S), at(A,(Y1,X1),S+1), X!=X1, trans_count((Y,X),D,N), conv(D,(DY,DX)), N=1.
% forward on switches
action(A,2,S) :- entered_from(A,(Y,X+DX),S), at(A,(Y,X),S), at(A,(Y,_),S+1), trans_count((Y,X),D,N), conv(D,(0,DX)), N>=2.
action(A,2,S) :- entered_from(A,(Y+DY,X),S), at(A,(Y,X),S), at(A,(_,X),S+1), trans_count((Y,X),D,N), conv(D,(DY,0)), N>=2.
```
For the forward action (2) two cases have to be addressed, moving forward off and on switches. In the case of no switches (`N`=1), any change in position is automatically a forward movement and action.     
If there are switches (`N`>=2), movement only along the X-axis (Y coordinate remains constant) or Y-axis (X coordinate remains constant) clearly shows a forward movement and action.

```
% right: 3
action(A,3,S) :- entered_from(A,(Y,X-DX),S), at(A,(Y,X),S), at(A,(Y+DY,X),S+1), turn(DY,DX), DY+DX!=0, trans_count((Y,X),D,N), conv(D,(0,-DX)), N>=2.
action(A,3,S) :- entered_from(A,(Y-DY,X),S), at(A,(Y,X),S), at(A,(Y,X+DX),S+1), turn(DY,DX), DY+DX=0, trans_count((Y,X),D,N), conv(D,(-DY,0)), N>=2.
% stop: 4
action(A,4,S) :- at(A,C,S), at(A,C,S+1). 
```
The last two actions can be found above. The right turn (3) is the same as the left turn, just the order of steps corresponding to the sum of `DY` and `DX` is switched.     
The wait action (4) can simply be inferred by no change in the position of subsequent steps.

```
#minimize{1,S,A: at(A,_,S)}.
%#show entered_from/3.
#show at/3.
#show action/3.
```
The minimization above guarantees an optimal solution with no useless "wait" actions and the fastest path to the target. The other lines are for debugging and output generation, which can be interpreted by our tools.

## scheduler_dev.lp

`scheduler_dev.lp` tries different approaches to optimize the above encoding. 2 approaches have been tested so far.
```
0{at(A,(Y2,X2),S) : cell(Y2,X2), at(A,(Y1,X1),S-1), |Y1-Y2|+|X1-X2|<=1}1 :- agent(A), step(S).
```
In the first approach above the generation of possible positions (`at/3`) is limited to neighbouring cells with tracks instead of all cells with tracks of the instance.  
The additional removal of the constraint which checks for valid moves only to neighbouring cells does not result in a performance increase.

```
% add transitions for waiting
trans(C1,C2,C2) :- trans(C1,C2,_).
% limit to valid transitions
0{at(A,C3,S) : trans(C1,C2,C3), entered_from(A,C1,S-1), at(A,C2,S-1)}1 :- agent(A), step(S).

```
This approach was further improved by limiting possible positions to cells with valid transitions. To be able to allow agents to remain in their position the transitions had to be expanded. Similar to above, removing the constraints regarding path validation does not improve run-time but even hurts it. 

```
% first decide if stay (wait) or not
0{stay(A,S) : at(A,_,S-1)}1 :- agent(A), step(S).
at(A,C,S) :- at(A,C,S-1), stay(A,S).
% limit to valid transitions if not stayed
0{at(A,C3,S) : trans(C1,C2,C3), entered_from(A,C1,S-1), at(A,C2,S-1)}1 :- agent(A), step(S), not stay(A,S).
```
The second approach splits waiting and moving. First possible `stay(A,S)` predicates are generated, which denotes that agent `A` stays in its previous position at step `S`, which results in the positions in the next line. For all remaining steps, possible positions (moves) can then be derived by the valid transitions.   
The removal of the corresponding constraint can have varying effects depending on instance size.

Preliminary testing shows, that the first approach halves the run-time, while the second approach is faster than the original encoding but scales worse. For a final conclusion, more testing is required.   
In the table below the preliminary results can be seen with a step limit of 30. opt val denotes the number of occupied positions for all agents in the optimal solution and gives an estimate of the required computations. The other columns show the required run-time for the optimal solution in seconds. The value in parenthesis is the run-time of the improved approach.  

instance | opt val | original | 1st appr | 1st appr w/o cons | 2nd appr | 2nd appr w/o cons
:---|---:|---:|---:|---:|---:|---:
7x7x4-wait | 52 | 13 | 6 (5) | 8 (8) | 5 | 2 
7x7x4-circle | 100 | 29 | 14 (13) | 15 (36) | 18 | 30

## Benchmarking

For benchmarking, we will compare the original encoding and the first approach described above. The original encoding is given version number 1.0, while the first approach and its improvement get the numbers 1.1 and 1.2 respectively. Encodings without `unneeded` constraints are marked with `nc`. A detailed explanation of our testing methodology and our results can be found in `/testing/'.  
