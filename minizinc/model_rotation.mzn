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
% array of booleans to allow rotation
array[1..num_plates] of var bool: rotation;

%apply_rotation
array[1..num_plates] of var int: plates_x_r = [if plates_x[i] != plates_y[i] /\ rotation[i] then
  plates_y[i] else
  plates_x[i] endif | i in 1..num_plates];
  
array[1..num_plates] of var int: plates_y_r = [if plates_x[i] != plates_y[i] /\ rotation[i] then 
  plates_x[i] else
  plates_y[i] endif | i in 1..num_plates];
 
var int: length = max([y[i] + plates_y_r[i] | i in 1..num_plates]); 
var int: max_width = max([x[i] + plates_x_r[i] | i in 1..num_plates]);
% domains of values in x
constraint forall(i in 1..num_plates)(x[i] >= 0 /\ x[i] <= width - plates_x_r[i]);
% domains of values in y
constraint forall(i in 1..num_plates)(y[i] >= 0 /\ y[i] <= length - plates_y_r[i]);

% no overlap
constraint forall(i, j in 1..num_plates where i < j) (
  x[i] + plates_x_r[i] <= x[j] \/
  x[j] + plates_x_r[j] <= x[i] \/
  y[i] + plates_y_r[i] <= y[j] \/
  y[j] + plates_y_r[j] <= y[i]);

% upper bound on the width
constraint max_width <= width;

% no packing constraint
constraint forall(i, j in 1..num_plates where i < j)(
    ((plates_x_r[i] + plates_x_r[j] > width) -> ((y[j] >= y[i] + plates_y_r[i]) \/ 
      (y[i] >= y[j] + plates_y_r[j]))) /\ 
    ((plates_y_r[i] + plates_y_r[j] > length) -> ((x[j] >= x[i] + plates_x_r[i]) \/
      (x[i] >= x[j] + plates_x_r[j])))
  );
  
% impose ordering between plates with equal size

constraint symmetry_breaking_constraint(forall(i, j in 1..num_plates where i < j)(
    (plates_x_r[i] == plates_x_r[j] /\ plates_y_r[i] == plates_y_r[j]) ->
    not(x[j] < x[i] /\ ((x[j] > x[i]) \/ not(y[j] < y[i])))));

% smaller circuits should be to the right or above bigger ones

constraint symmetry_breaking_constraint(forall(i, j in 1..num_plates where i < j) (
    ((areas[i] < areas[j]) -> (x[i] > x[j] \/ y[i] > y[j]))
   ));

% further reduce the domain of the "biggest" circuits
% along the x dimension

/*
int: max_idx_w = arg_max([plates_x_r[i] | i in 1..num_plates]);

constraint (
  x[max_idx_w] >= 0 /\ x[max_idx_w] <= ((width - plates_x_r[max_idx_w]) div 2)
  );

% along the y dimension
int: max_idx_l = arg_max([plates_y_r[i] | i in 1..num_plates]);
constraint (
  y[max_idx_l] >= 0 /\ y[max_idx_l] <= ((length - plates_y_r[max_idx_l]) div 2)
  );
*/

solve minimize length;

output [show(width) ++ " " ++ show(length) ++ "\n" ++
        show(num_plates) ++ "\n"] ++ 
        [show(plates_x[i]) ++ " " ++ show(plates_y[i]) ++ " " ++
         show(x[i]) ++ " " ++ show(y[i]) ++ " " ++ 
         show(rotation[i]) ++ " \n"| i in 1..num_plates];
