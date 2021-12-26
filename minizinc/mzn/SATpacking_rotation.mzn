include "diffn.mzn";

int: w;
int: width = w+1; %solver finds solution for w-1, so the incrementation allows us to find solution for w (width is only used for generators)
int: num_of_circuits;
set of int: NCIRCUITS = 1..num_of_circuits;
array[NCIRCUITS,1..2] of int: size;

function int: get_index(array[NCIRCUITS,1..2] of int: size, int: max_width, int: pos, int: max_val) =
	if pos > num_of_circuits then max_val
	else if max_width == size[pos,1] then get_index(size,max_width,pos+1,pos)
	else get_index(size,max_width,pos+1,max_val)
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
function int: get_sum_height(array[NCIRCUITS,1..2] of int: size, int: i, int: s) =
        if i > num_of_circuits then s
        else if size[i,1] > size[i,2] then get_sum_height(size,i+1,s+size[i,1])
        else get_sum_height(size,i+1,s+size[i,2])
        endif
        endif;
        
function int: get_max_dim(array[NCIRCUITS,1..2] of int: size, int: i, int: m) =
        if i > num_of_circuits then m
        else if size[i,1] > size[i,2] /\ size[i,1] > m then get_max_dim(size,i+1,size[i,1])
        else if size[i,2] >= size[i,1] /\ size[i,2] > m then get_max_dim(size,i+1,size[i,2])
        else get_max_dim(size,i+1,m)
        endif
        endif
        endif;

int: sum_height = get_sum_height(size,1,0);
int: max_height = get_max_dim(size,1,0);
int: max_width = max_height;
array[NCIRCUITS] of int: max_size = [if size[i,1] > size[i,2] then size[i,1] else size[i,2] endif | i in NCIRCUITS];
array[NCIRCUITS] of int: min_size = [if size[i,1] > size[i,2] then size[i,2] else size[i,1] endif | i in NCIRCUITS];


%constraint forall(i in NCIRCUITS)(
%  if size[i,1] > size[i,2] then max_size[i] = size[i,1]
%  else max_size[i] = size[i,2]
%  endif
%);

%constraint forall(i in NCIRCUITS)(
%  if size[i,1] > size[i,2] then min_size[i] = size[i,2]
%  else min_size[i] = size[i,1]
%  endif
%);



array[NCIRCUITS,NCIRCUITS] of var bool: lr; % true if the i-th block is at the left of j 
array[NCIRCUITS,NCIRCUITS] of var bool: ud; % true if the i-th block is below j
array[NCIRCUITS,0..width] of var bool: px; % true if the i-th block is at the left of e, where e is an int that spans the width
array[NCIRCUITS,0..sum_height] of var bool: py; % true if the i-th block is below f, where f is an int that spans the sum of all the heights 
array[max_height..sum_height] of var bool: ph; % true if the int o is above all the blocks
array[NCIRCUITS] of var bool: rotation; %1 -> width and height are swapped, 0 otherwise

int: max_width_index = get_index(size,max_width,1,1);

%order encoding

constraint forall(i in NCIRCUITS)( %first column is always false, in order to help the overlapping constraint over the leftmost block
	not(px[i,0])
);

constraint forall(i in NCIRCUITS)( %same here
 not(py[i,0])   
);

%order constraints

constraint forall(i in NCIRCUITS, e in 0..width-min_size[i]-1)(
	not(px[i,e]) \/ px[i,e+1]
);

constraint forall(i in NCIRCUITS, f in 0..sum_height-min_size[i]-1)(
 not(py[i,f]) \/ py[i,f+1]
);

%the e and f in which the i-th block overlaps the maximum width and height must be true

constraint forall(i in NCIRCUITS, e in width-(size[i,1]*(1-rotation[i]))-(size[i,2]*rotation[i])..width)(
        if e > 0 then px[i,e] endif
);

constraint forall(i in NCIRCUITS, f in sum_height-(size[i,2]*(1-rotation[i]))-(size[i,1]*rotation[i])..sum_height)(
	py[i,f]
);

%no overlapping

constraint forall(i in NCIRCUITS, j in i+1..num_of_circuits)( %block i must be either left, right, down, above the block j
	lr[i,j] \/ lr[j,i] \/ ud[i,j] \/ ud[j,i]
);

constraint forall(i in NCIRCUITS, j in i+1..num_of_circuits, e in 0..width-(size[i,1]*(1-rotation[i]))-(size[i,2]*rotation[i]))(
	%if i is to the left of j, and if e is before i-th starting point, then e + the width of i must be before the starting point of j
	not(lr[i,j]) \/ px[i,e] \/ not(px[j,(e+size[i,1])*(1-rotation[i])] \/ px[j,(e+size[i,2])*(rotation[i])])
);

constraint forall(i in NCIRCUITS, j in i+1..num_of_circuits, f in 0..sum_height-(size[j,2]*(1-rotation[j]))-(size[j,1]*rotation[j]))(
	%same here
	not(ud[j,i]) \/ py[j,f] \/ not(py[i,(f+size[j,2])*(1-rotation[j])] \/ py[i,(f+size[j,1])*(rotation[j])])
);

constraint forall(i in NCIRCUITS, j in i+1..num_of_circuits, e in 0..width-(size[j,1]*(1-rotation[j]))-(size[j,2]*rotation[j]))(
	%same here
	not(lr[j,i]) \/ px[j,e] \/ not(px[i,(e+size[j,1])*(1-rotation[j])] \/ px[i,(e+size[j,2])*(rotation[j])])
);

constraint forall(i in NCIRCUITS, j in i+1..num_of_circuits, f in 0..sum_height-(size[i,2]*(1-rotation[i]))-(size[i,1]*rotation[i]))(
	%same here
	not(ud[i,j]) \/ py[i,f] \/ not(py[j,(f+size[i,2])*(1-rotation[i])] \/ py[j,(f+size[i,1])*(rotation[i])]) 
);

%order constraint

constraint forall (o in max_height..sum_height-1)(
	not(ph[o]) \/ ph[o+1]
);

%if o is above all the blocks, then o - the height of i must be above i's starting point

constraint forall (o in max_height+1..sum_height-1, i in NCIRCUITS)(
	not(ph[o]) \/ (py[i,(o-size[i,2])*(1-rotation[i])] \/ py[i,(o-size[i,1])*(rotation[i])])
);

%speeding up constraints
%if the sum of the widths of 2 circuits is higher than the width of the plate, then the circuits can't be to the left of the other or viceversa

%constraint forall(i in NCIRCUITS, j in i+1..num_of_circuits)(
% if size[i,1] + size[j,1] > w then not(lr[i,j]) /\ not(lr[j,i]) endif
%);

%constraint forall(e in ((width-size[max_width_index,1]) div 2)..width-size[max_width_index,1])(
%	px[max_width_index,e] %solve reduction for circuit with max width, simmetry breaking
%);

%if we have 2 circuits with same width and height, we impose an ordering (symmetry breaking)
%constraint forall(i in NCIRCUITS, j in i+1..num_of_circuits)(
% if size[i,1] == size[j,1] /\ size[i,2] == size[j,2] then not(lr[j,i]) /\ (lr[i,j] \/ not(ud[j,i])) endif
%);

var int: final_height = height(ph,max_height); %find position in which ph[o] switches from false to true (height that contains each block)

solve :: int_search(rotation, dom_w_deg, indomain_random, complete)

minimize final_height;

%output ["height=", show(final_height),"\n"];
