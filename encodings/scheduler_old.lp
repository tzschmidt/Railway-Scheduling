
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
:- at(A,(Y,X),S1), at(A,(Y2,X2),S2), S1<S2, Y!=Y2, target(A,(Y,X)), agent(A).
:- at(A,(Y,X),S1), at(A,(Y2,X2),S2), S1<S2, X!=X2, target(A,(Y,X)), agent(A).

% no collisions
% vertex
:- at(A1,(Y,X),S), at(A2,(Y,X),S), step(S), agent(A1), agent(A2), A1!=A2.
% edge
:- at(A1,(Y1,X1),S), at(A2,(Y2,X2),S), at(A1,(Y2,X2),S-1), at(A2,(Y1,X1),S-1),
	step(S), agent(A1), agent(A2), A1!=A2.

% only valid actions
% move to neighbors or wait
:- at(A,(Y1,X1),S-1), at(A,(Y2,X2),S), |Y1-Y2|+|X1-X2|>1, step(S), agent(A). 
% continueous
:- not at(A,_,S-1), at(A,_,S), step(S), agent(A). 
% transitions
:- at(A,(Y1,X1),S-1), at(A,(Y2,X2),S), at(A,(Y3,X3),S+1), not trans((Y1,X1),(Y2,X2),(Y3,X3)),
	step(S), agent(A).

% TODO:
% - get actions(move, wait, turn)

#minimize{1,S: at(_,_,S)}.
#show at/3. 
