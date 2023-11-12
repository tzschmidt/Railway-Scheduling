% directions
% north
conv(0,(-1,0)).
% east
conv(1,(0,1)).
% south
conv(2,(1,0)).
% west
conv(3,(0,-1)).

% transitions
trans((Y+DY1,X+DX1),(Y,X),(Y+DY2,X+DX2)) :- transraw((Y,X),D1,D2), conv(D1,(DY1, DX1)), conv(D2,(DY2,DX2)).

% turns:
turn(-1,1).
turn(1,1).
turn(1,-1).
turn(-1,-1).
