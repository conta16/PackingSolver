include "diffn.mzn";

int: W;
int: plate_width = W+1; %solver finds solution for w-1, so the incrementation allows us to find solution for w (width is only used for generators)
int: N;
set of int: NCIRCUITS = 1..N;
array[NCIRCUITS] of int: width;
array[NCIRCUITS] of int: height;


function var int: get_index(array[NCIRCUITS] of var int: arr, var int: max_arr, int: pos, int: max_pos) =
	if pos > N then max_pos
	else if max_arr == arr[pos] then get_index(arr,max_arr,pos+1,pos)
	else get_index(arr,max_arr,pos+1,max_pos)
	endif
	endif;
		
% used to get the height from the ph array
function var int: height(array[max_height..sum_height] of var bool: ph, int: pos) =
	if pos == sum_height then pos
	else if ph[pos] != ph[pos+1] then pos
	else height(ph,pos+1)
	endif
	endif;

% get total height if I stack each block on the highest dimension
function int: get_sum_height(array[NCIRCUITS] of int: width, array[NCIRCUITS] of int: height, int: i, int: s) =
        if i > N then s
        else if width[i] > height[i] then get_sum_height(width,height,i+1,s+width[i])
        else get_sum_height(width,height,i+1,s+height[i])
        endif
        endif;
        
function int: get_max_dim(array[NCIRCUITS] of int: width, array[NCIRCUITS] of int: height, int: i, int: m) = %max between all dimensions
        if i > N then m
        else if width[i] > height[i] /\ width[i] > m then get_max_dim(width,height,i+1,width[i])
        else if height[i] >= width[i] /\ height[i] > m then get_max_dim(width,height,i+1,height[i])
        else get_max_dim(width,height,i+1,m)
        endif
        endif
        endif;
        
function var int: get_max_width(array[NCIRCUITS] of var int: width, int: i, var int: m) =
        if i > N then m
        else if width[i] > m then get_max_width(width,i+1,width[i])
        else get_max_width(width,i+1,m)
        endif
        endif;

int: sum_height = get_sum_height(width,height,1,0);
int: max_height = get_max_dim(width,height,1,0);
array[NCIRCUITS] of int: max_size = [if width[i] > height[i] then width[i] else height[i] endif | i in NCIRCUITS];
array[NCIRCUITS] of int: min_size = [if width[i] > height[i] then height[i] else width[i] endif | i in NCIRCUITS];



array[NCIRCUITS,NCIRCUITS] of var bool: lr; % true if the i-th block is at the left of j 
array[NCIRCUITS,NCIRCUITS] of var bool: ud; % true if the i-th block is below j
array[NCIRCUITS,0..plate_width] of var bool: px; % true if the i-th block is at the left of e, where e is an int that spans the width
array[NCIRCUITS,0..sum_height] of var bool: py; % true if the i-th block is below f, where f is an int that spans the sum of all the heights 
array[max_height..sum_height] of var bool: ph; % true if the int o is above all the blocks
array[NCIRCUITS] of var bool: rotation; %1 -> width and height are swapped, 0 otherwise

%order encoding

constraint forall(i in NCIRCUITS)( %first column is always false, in order to help the overlapping constraint over the leftmost block
	not(px[i,0])
);

constraint forall(i in NCIRCUITS)( %same here
 not(py[i,0])   
);

%order constraints

constraint forall(i in NCIRCUITS, e in 0..plate_width-min_size[i]-1)(
	not(px[i,e]) \/ px[i,e+1]
);

constraint forall(i in NCIRCUITS, f in 0..sum_height-min_size[i]-1)(
 not(py[i,f]) \/ py[i,f+1]
);

%the e and f in which the i-th block overlaps the maximum width and height must be true

constraint forall(i in NCIRCUITS, e in plate_width-(width[i]*(1-rotation[i]))-(height[i]*rotation[i])..plate_width)(
        if e > 0 then px[i,e] endif
);

constraint forall(i in NCIRCUITS, f in sum_height-(height[i]*(1-rotation[i]))-(width[i]*rotation[i])..sum_height)(
	py[i,f]
);

%no overlapping

constraint forall(i in NCIRCUITS, j in i+1..N)( %block i must be either left, right, down, above the block j
	lr[i,j] \/ lr[j,i] \/ ud[i,j] \/ ud[j,i]
);

constraint forall(i in NCIRCUITS, j in i+1..N, e in 0..plate_width-(width[i]*(1-rotation[i]))-(height[i]*rotation[i]))(
	%if i is to the left of j, and if e is before i-th starting point, then e + the width of i must be before the starting point of j
	not(lr[i,j]) \/ px[i,e] \/ not(px[j,(e+width[i])*(1-rotation[i])] \/ px[j,(e+height[i])*(rotation[i])])
);

constraint forall(i in NCIRCUITS, j in i+1..N, f in 0..sum_height-(height[j]*(1-rotation[j]))-(width[j]*rotation[j]))(
	%same here
	not(ud[j,i]) \/ py[j,f] \/ not(py[i,(f+height[j])*(1-rotation[j])] \/ py[i,(f+width[j])*(rotation[j])])
);

constraint forall(i in NCIRCUITS, j in i+1..N, e in 0..plate_width-(width[j]*(1-rotation[j]))-(height[j]*rotation[j]))(
	%same here
	not(lr[j,i]) \/ px[j,e] \/ not(px[i,(e+width[j])*(1-rotation[j])] \/ px[i,(e+height[j])*(rotation[j])])
);

constraint forall(i in NCIRCUITS, j in i+1..N, f in 0..sum_height-(height[i]*(1-rotation[i]))-(width[i]*rotation[i]))(
	%same here
	not(ud[i,j]) \/ py[i,f] \/ not(py[j,(f+height[i])*(1-rotation[i])] \/ py[j,(f+width[i])*(rotation[i])]) 
);

%order constraint

constraint forall (o in max_height..sum_height-1)(
	not(ph[o]) \/ ph[o+1]
);

%if o is above all the blocks, then o - the height of i must be above i's starting point

constraint forall (o in max_height+1..sum_height-1, i in NCIRCUITS)(
	not(ph[o]) \/ (py[i,(o-height[i])*(1-rotation[i])] \/ py[i,(o-width[i])*(rotation[i])])
);

%speeding up constraints
%if the sum of the widths of 2 circuits is higher than the width of the plate, then the circuits can't be to the left of the other or viceversa

array[1..N] of var int: width_rotated = [if rotation[i] then height[i] else width[i] endif | i in 1..N];
array[1..N] of var int: height_rotated = [if rotation[i] then width[i] else height[i] endif | i in 1..N];

constraint forall(i in NCIRCUITS, j in i+1..N)(
 if width_rotated[i] + width_rotated[j] > W then not(lr[i,j]) /\ not(lr[j,i]) endif
);

var int: max_width = get_max_width(width_rotated,1,0);
var int: max_width_index = get_index(width_rotated,max_width,1,1);

constraint forall(e in ((plate_width-width[max_width_index]) div 2)..plate_width-width[max_width_index])(
	px[max_width_index,e] %solve reduction for circuit with max width, simmetry breaking
);

%if we have 2 circuits with same width and height, we impose an ordering (symmetry breaking)
constraint forall(i in NCIRCUITS, j in i+1..N)(
 if width_rotated[i] == width_rotated[j] /\ height_rotated[i] == height_rotated[j] then not(lr[j,i]) /\ (lr[i,j] \/ not(ud[j,i])) endif
);

var int: final_height = height(ph,max_height); %find position in which ph[o] switches from false to true (height that contains each block)

solve

minimize final_height;

%output ["height=", show(final_height),"\n"];
