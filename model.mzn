% Use this editor as a MiniZinc scratch book
int: width;
int: num_plates;
% width of each plate
array[1..num_plates] of int: plates_x;
% height of each plate
array[1..num_plates] of int: plates_y;
% compute areas of plates
array[1..num_plates] of int: areas = [plates_x[i]*plates_y[i]|i in 1..num_plates];
% x coordinates of the bottom-left corners
array[1..num_plates] of var int: x;
% y coordinates of the bottom-left corners
array[1..num_plates] of var int: y;

var 1..sum(plates_y): length = max([y[i] + plates_y[i] | i in 1..num_plates]); 

% domains of values in x
constraint forall(i in 1..num_plates)(x[i] >= 0 /\ x[i] <= width - plates_x[i]);
% domains of values in y
constraint forall(i in 1..num_plates)(y[i] >= 0 /\ y[i] <= length - plates_y[i]);

% no overlap
constraint forall(i, j in 1..num_plates where i != j) (
  x[i] + plates_x[i] <= x[j] \/
  x[j] + plates_x[j] <= x[i] \/
  y[i] + plates_y[i] <= y[j] \/
  y[j] + plates_y[j] <= y[i]);

% upper bound on the width
constraint forall(i in 1..num_plates)(
  x[i] + plates_x[i] <= width 
);

% no packing constraint
constraint forall(i, j in 1..num_plates where i != j)(
    ((plates_x[i] + plates_x[j] > width) -> y[i] != y[j]) /\ 
    ((plates_y[i] + plates_y[j] > length) -> x[i] != x[j])
  );
  
% impose ordering between plates with equal size

constraint forall(i, j in 1..num_plates where i != j)(
    (plates_x[i] == plates_x[j] /\ plates_y[i] == plates_y[j]) ->
    (x[i] < x[j] /\ y[i] < y[j]));

% smaller circuits should be to the right or above bigger ones

constraint forall(i, j in 1..num_plates where i != j) (
    ((areas[i] < areas[j]) -> (x[i] > x[j] \/ y[i] > y[j]))
   );
    
solve minimize length;
output [show(width) ++ " " ++ show(length) ++ "\n" ++
        show(num_plates) ++ "\n"] ++ 
        [show(plates_x[i]) ++ " " ++ show(plates_y[i]) ++ " " ++
          show(x[i]) ++ " " ++ show(y[i]) ++ "\n" | i in 1..num_plates];

