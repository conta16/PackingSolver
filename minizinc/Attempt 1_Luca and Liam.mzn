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


% Constraint ensuring that along the y-direction there is not a single scenario where the arranged circuits as they might get stacked side-by-side never exceeds the maximum allowable width (W) of the bigger rectangular plate.
constraint forall (y_iterator in 1..Height) 
(sum ([width[i] | i in 1..N where y_coordinate[i]<y_iterator /\ y_iterator<=height[i]+y_coordinate[i] ])<= W);

% Constraint for ensuring that none of the circuits are haivng a width more than the width of bigger rectangular plate
% This is an implied constraints
constraint forall (i in 1..N) 
(width[i] <= W);

% Constraint for ensuring that none of the circuits are haivng a height more than the height of bigger rectangular plate. This height we are trying to optimize.

% This is an implied constraints
constraint forall (i in 1..N) 
(height[i] <= Height);


% Non-negativity constraints:Since (0,0) has been taken to the reference for measuring the co-ordinates

constraint forall (i in 1..N) (x_coordinate[i]>=0);
constraint forall (i in 1..N) (y_coordinate[i]>=0);

%Implied constraints

% A circuit board cannot begin at the end of the maximum height that shall get computed and something we are trying to optimize.
constraint forall (i in 1..N) (y_coordinate[i]<Height);
% A circuit board cannot begin at the end of the prescribed width
constraint forall (i in 1..N) (x_coordinate[i]<W);

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

% Symmetry Breaking constraints.
% Type : 1 : When there be multiple circuit boards of same dimensions which when being swapped shall result in symmetric solutions

%constraint forall (i in 1..N, j in 1..N where i!=j)
%(
%if (width[i] == width[j] /\ height[i] == height[j]) then

%lex_greater([x_coordinate[i], y_coordinate[i]],[x_coordinate[j], y_coordinate[j]])

%endif);

% Symmetry Breaking constraints.
% Type : 2 : Mirror Reflection. 
% The symmety breaking in this case is being indirectly tackled by thinking that symmetric solutions are being produced by flipping operation.
% If flipping results in Mirror reflection, then for all circuit boards whose left bottom corner shall have abscissa value lesser than Floor(W/2)
% in the mirror reflected symmetric version, would have abscissa value greater than Floor(W/2) and conversely.

%array[1..N] of var 0..W-1: x_Flipped_coordinate; 

%constraint forall(i in 1..N) 
%(
%x_Flipped_coordinate[i] = W- sum([width[j] | j in 1..N where y_coordinate[i]==y_coordinate[j] /\ x_coordinate[i] > x_coordinate[j]])

%);

%float:K;
%K = (W div 2);

%constraint forall (i in 1..N)
%(
%if (x_coordinate[i] < K) then

%lex_greater([x_coordinate[i]],[x_Flipped_coordinate[i]])

%endif);



% Symmetry Breaking constraints.
% Type : 3 : Swapping of rows. 
% The symmety breaking in this case is being indirectly tackled by not allowing any smaller circuit board is below any bigger one.

%constraint forall (i in 1..N, j in 1..N where i!=j)
%(
%if (width[i] < width[j]) then

%lex_greater([y_coordinate[i]],[y_coordinate[j]])

%endif);


% We minimize Height. 
solve minimize Height;

%output [" Height= \(Height)"];
