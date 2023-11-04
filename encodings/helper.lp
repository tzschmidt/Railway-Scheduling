
% north -> north
trans((Y-1,X),(Y,X),(Y-1,X)) :- transraw((Y,X),0,0).
% north -> east
trans((Y-1,X),(Y,X),(Y,X+1)) :- transraw((Y,X),0,1).
% north -> south
trans((Y-1,X),(Y,X),(Y+1,X)) :- transraw((Y,X),0,2).
% north -> west
trans((Y-1,X),(Y,X),(Y,X-1)) :- transraw((Y,X),0,3).
% east -> north
trans((Y,X+1),(Y,X),(Y-1,X)) :- transraw((Y,X),1,0).
% east -> east
trans((Y,X+1),(Y,X),(Y,X+1)) :- transraw((Y,X),1,1).
% east -> south
trans((Y,X+1),(Y,X),(Y+1,X)) :- transraw((Y,X),1,2).
% east -> west
trans((Y,X+1),(Y,X),(Y,X-1)) :- transraw((Y,X),1,3).
% south -> north
trans((Y+1,X),(Y,X),(Y-1,X)) :- transraw((Y,X),2,0).
% south -> east
trans((Y+1,X),(Y,X),(Y,X+1)) :- transraw((Y,X),2,1).
% south -> south
trans((Y+1,X),(Y,X),(Y+1,X)) :- transraw((Y,X),2,2).
% south -> west
trans((Y+1,X),(Y,X),(Y,X-1)) :- transraw((Y,X),2,3).
% west -> north
trans((Y,X-1),(Y,X),(Y-1,X)) :- transraw((Y,X),3,0).
% west -> east
trans((Y,X-1),(Y,X),(Y,X+1)) :- transraw((Y,X),3,1).
% west -> south
trans((Y,X-1),(Y,X),(Y+1,X)) :- transraw((Y,X),3,2).
% west -> west
trans((Y,X-1),(Y,X),(Y,X-1)) :- transraw((Y,X),3,3).





