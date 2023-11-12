
% step limit
#const slimit=10.

step(1..slimit).

% start positions
at(A,(Y,X),0) :- agent(A), starting(A,(Y,X)).

% generate positions
0{at(A,(Y,X),S) : cell((Y,X),_)}1 :- agent(A), step(S).

% finish at target
:- not at(A,(Y,X),_), target(A,(Y,X)), agent(A).
% dont move away from target
:- at(A,C,S1), at(A,C1,S2), S1<S2, C!=C1, target(A,C), agent(A).

% no collisions
% vertex
:- at(A1,(Y,X),S), at(A2,(Y,X),S), step(S), agent(A1), agent(A2), A1!=A2.
% edge
:- at(A1,(Y1,X1),S), at(A2,(Y2,X2),S), at(A1,(Y2,X2),S-1), at(A2,(Y1,X1),S-1),
	step(S), agent(A1), agent(A2), A1!=A2.

% keep track of orientation via cell which agent entered from
% starting direction
entered_from(A,(Y-DY,X-DX),0) :- starting(A,(Y,X)), direction(A,D), conv(D,(DY,DX)).
% wait
entered_from(A,(Y1,X1),S) :- at(A,(Y,X),S), at(A,(Y,X),S-1), entered_from(A,(Y1,X1),S-1), agent(A), step(S).
% move
entered_from(A,C,S) :- at(A,C1,S), at(A,C,S-1), C!=C1, agent(A), step(S).

% only valid actions
% move to neighbors or wait
:- at(A,(Y1,X1),S-1), at(A,(Y2,X2),S), |Y1-Y2|+|X1-X2|>1, step(S), agent(A). 
% continueous
:- not at(A,_,S-1), at(A,_,S), step(S), agent(A). 
% transitions
:- entered_from(A,(Y1,X1),S-1), at(A,(Y2,X2),S-1), at(A,(Y3,X3),S), not trans((Y1,X1),(Y2,X2),(Y3,X3)), step(S), agent(A).

% actions:
% none: 0
% left: 1
action(A,1,S) :- at(A,(Y,X+DX),S-1), at(A,(Y,X),S), at(A,(Y+DY,X),S+1), turn(DY,DX), DY+DX=0, cell((Y,X),N), N>=3.
action(A,1,S) :- at(A,(Y+DY,X),S-1), at(A,(Y,X),S), at(A,(Y,X+DX),S+1), turn(DY,DX), DY+DX!=0, cell((Y,X),N), N>=3.
% forward: 2
action(A,2,S) :- at(A,C,S), at(A,C1,S+1), C!=C1, cell(C,N), N<=2.
% foward on switches
action(A,2,S) :- at(A,(Y,_),S-1), at(A,(Y,_),S), at(A,(Y,_),S+1), cell((Y,X),N), N>=3.
action(A,2,S) :- at(A,(_,X),S-1), at(A,(_,X),S), at(A,(_,X),S+1), cell((Y,X),N), N>=3.
% right: 3
action(A,3,S) :- at(A,(Y,X+DX),S-1), at(A,(Y,X),S), at(A,(Y+DY,X),S+1), turn(DY,DX), DY+DX!=0, cell((Y,X),N), N>=3.
action(A,3,S) :- at(A,(Y+DY,X),S-1), at(A,(Y,X),S), at(A,(Y,X+DX),S+1), turn(DY,DX), DY+DX=0, cell((Y,X),N), N>=3.
% stop: 4
action(A,4,S) :- at(A,C,S), at(A,C,S+1). 

#minimize{1,S: at(_,_,S)}.
#show entered_from/3.
#show at/3.
#show action/3.
