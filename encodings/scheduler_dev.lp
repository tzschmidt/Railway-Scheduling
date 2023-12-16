
% step limit
#const slimit=20.

step(1..slimit).

% start positions
at(A,(Y,X),0) :- agent(A), starting(A,(Y,X)).

% generate positions
% limit to neighbors
0{at(A,(Y2,X2),S) : cell(Y2,X2), at(A,(Y1,X1),S-1), |Y1-Y2|+|X1-X2|<=1}1 :- agent(A), step(S).

% first decide if stay (wait) or not
%0{stay(A,S) : at(A,_,S-1)}1 :- agent(A), step(S).
%at(A,C,S) :- at(A,C,S-1), stay(A,S).
% limit to valid transitions if not stayed
%0{at(A,C3,S) : trans(C1,C2,C3), entered_from(A,C1,S-1), at(A,C2,S-1)}1 :- agent(A), step(S), not stay(A,S).

% finish at target
:- not at(A,(Y,X),_), target(A,(Y,X)), agent(A).
% dont move away from target
:- at(A,C,S1), at(A,_,S2), S1<S2, target(A,C), agent(A).

% no collisions
% vertex
:- at(A1,(Y,X),S), at(A2,(Y,X),S), step(S), agent(A1), agent(A2), A1!=A2.
% edge
:- at(A1,(Y1,X1),S), at(A2,(Y2,X2),S), at(A1,(Y2,X2),S-1), at(A2,(Y1,X1),S-1),
	step(S), agent(A1), agent(A2), A1!=A2.

% keep track of orientation via cell which agent entered from
% starting direction
entered_from(A,(Y-DY,X-DX),0) :- starting(A,(Y,X)), direction(A,D), conv(D,(DY,DX)), trans((Y-DY,X-DX),(Y,X),_).
% dead-end
entered_from(A,(Y+DY,X+DX),0) :- starting(A,(Y,X)), direction(A,D), conv(D,(DY,DX)), not trans((Y-DY,X-DX),(Y,X),_).
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
:- entered_from(A,C1,S-1), at(A,C2,S-1), at(A,C3,S), C2!=C3, not trans(C1,C2,C3), step(S), agent(A).

% actions:
% none: 0
% left: 1
action(A,1,S) :- entered_from(A,(Y,X-DX),S), at(A,(Y,X),S), at(A,(Y+DY,X),S+1), turn(DY,DX), DY+DX=0, trans_count((Y,X),D,N), conv(D,(0,-DX)), N>=2.
action(A,1,S) :- entered_from(A,(Y-DY,X),S), at(A,(Y,X),S), at(A,(Y,X+DX),S+1), turn(DY,DX), DY+DX!=0, trans_count((Y,X),D,N), conv(D,(-DY,0)), N>=2.
% forward: 2
action(A,2,S) :- entered_from(A,(Y+DY,X+DX),S), at(A,(Y,X),S), at(A,(Y1,X1),S+1), Y!=Y1, trans_count((Y,X),D,N), conv(D,(DY,DX)), N=1.
action(A,2,S) :- entered_from(A,(Y+DY,X+DX),S), at(A,(Y,X),S), at(A,(Y1,X1),S+1), X!=X1, trans_count((Y,X),D,N), conv(D,(DY,DX)), N=1.
% foward on switches
action(A,2,S) :- entered_from(A,(Y,X+DX),S), at(A,(Y,X),S), at(A,(Y,_),S+1), trans_count((Y,X),D,N), conv(D,(0,DX)), N>=2.
action(A,2,S) :- entered_from(A,(Y+DY,X),S), at(A,(Y,X),S), at(A,(_,X),S+1), trans_count((Y,X),D,N), conv(D,(DY,0)), N>=2.
% right: 3
action(A,3,S) :- entered_from(A,(Y,X-DX),S), at(A,(Y,X),S), at(A,(Y+DY,X),S+1), turn(DY,DX), DY+DX!=0, trans_count((Y,X),D,N), conv(D,(0,-DX)), N>=2.
action(A,3,S) :- entered_from(A,(Y-DY,X),S), at(A,(Y,X),S), at(A,(Y,X+DX),S+1), turn(DY,DX), DY+DX=0, trans_count((Y,X),D,N), conv(D,(-DY,0)), N>=2.
% stop: 4
action(A,4,S) :- at(A,C,S), at(A,C,S+1). 

#minimize{1,S,A: at(A,_,S)}.
%#show entered_from/3.
%#show trans/3.
#show at/3.
#show action/3.
