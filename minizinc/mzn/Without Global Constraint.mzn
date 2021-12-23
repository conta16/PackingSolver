% Use this editor as a MiniZinc scratch book
include "gecode.mzn";
include "globals.mzn";

int: W; % width (Width of the Bigger rectangular plate on which the smaller rectangular circuit boards must be fitted)
int: N; % no. of circuit boards to be placed

% For each of the circuit boards, the width (x_dimension) and height (y_dimension):

array[1..N] of int: width;
array[1..N] of int: height;

% For each of the circuit boards,the x-coordinates and y-coordinates:
% The left end corner of the Bigger rectangular plate has been assumed to have co-ordinate (0,0). 
% This is our reference frame for measuring the co-ordinates (abscissa and ordinate) of the circuit boards

array[1..N] of var 0..W-1: x_coordinate; 
array[1..N] of var 0..sum(height)-1: y_coordinate;

% Defining the objective function which we are trying to minimize

var 1..sum(height): Height = max([y_coordinate[i] + height[i]| i in 1..N]);

% This section of the code ensures that under no circumstances, the set of slabs can ever be beyond the maximum permissible width

constraint forall(i in 1..N)(
  x_coordinate[i] + width[i] <= W  
);

% This section of the ensures that under no circumstances, the set of slabs can ever go beyond the maximum height (Height) something which we are 
% trying to minimize

constraint forall(i in 1..N)(
  y_coordinate[i] + height[i] <= Height  
);

% non-overlapping constraints

constraint forall (i in 1..N, j in 1..N where i!=j) 
(

(x_coordinate[i] + width[i] <= x_coordinate[j])
\/
(x_coordinate[j] + width[j] <= x_coordinate[i])
\/
(y_coordinate[i] + height[i] <= y_coordinate[j])
\/
(y_coordinate[j] + height[j] <= y_coordinate[i])

);


% We minimize Height. 
solve minimize Height;

output [" Height= \(Height)",
      "\n x_coordinate= \(x_coordinate)",
      "\n y_coordinate= \(y_coordinate)",
      "\n width= \(width)",
      "\n height= \(height)"];


