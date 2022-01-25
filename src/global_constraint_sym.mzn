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


constraint cumulative(x_coordinate,width,height,Height); %implied constraints
constraint cumulative(y_coordinate,height,width,W); %implied constraints
constraint diffn(x_coordinate,y_coordinate,width,height);

% Symmetry Breaking constraints.
% Type : 1 : When there be multiple circuit boards of same dimensions which when being swapped shall result in symmetric solutions

constraint forall (i in 1..N, j in 1..N where i!=j)
(
if (width[i] == width[j] /\ height[i] == height[j]) then

lex_greater([x_coordinate[i], y_coordinate[i]],[x_coordinate[j], y_coordinate[j]])

endif);

% Symmetry Breaking constraints.
% Type : 3 : Swapping of rows. 
% The symmety breaking in this case is being indirectly tackled by not allowing any smaller circuit board is below any bigger one.

constraint forall (i in 1..N, j in 1..N where i!=j)
(
if (width[i] < width[j]) then

lex_greater([x_coordinate[i],y_coordinate[i]],[x_coordinate[j],y_coordinate[j]])

endif);


% We minimize Height. 
solve minimize Height;

output [" Height= \(Height)",
      "\n x_coordinate= \(x_coordinate)",
      "\n y_coordinate= \(y_coordinate)",
      "\n width= \(width)",
      "\n height= \(height)"];


