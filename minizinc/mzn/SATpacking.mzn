include "diffn.mzn";

int: W;
int: plate_width = W+1; %solver finds solution for w-1, so the incrementation allows us to find solution for w (width is only used for generators)
int: N;
set of int: NCIRCUITS = 1..N;
%array[NCIRCUITS,1..2] of int: size;
array[NCIRCUITS] of int: width;
array[NCIRCUITS] of int: height;



int: sum_height = sum(i in NCIRCUITS)(height[i]);
int: max_height = max(i in NCIRCUITS)(height[i]);
int: max_width = max(i in NCIRCUITS)(width[i]);

array[NCIRCUITS,NCIRCUITS] of var bool: lr; % true if the i-th block is at the left of j 
array[NCIRCUITS,NCIRCUITS] of var bool: ud; % true if the i-th block is below j
array[NCIRCUITS,0..plate_width] of var bool: px; % true if the i-th block is at the left of e, where e is an int that spans the width
array[NCIRCUITS,0..sum_height] of var bool: py; % true if the i-th block is below f, where f is an int that spans the sum of all the heights 
array[max_height..sum_height] of var bool: ph; % true if the int o is above all the blocks

function int: get_index(array[NCIRCUITS] of int: width, array[NCIRCUITS] of int: height, int: max_width, int: pos, int: max_val) =
	if pos > N then max_val
	else if max_width == width[pos] then get_index(width,height,max_width,pos+1,pos)
	else get_index(width,height,max_width,pos+1,max_val)
	endif
	endif;
		

function var int: height(array[max_height..sum_height] of var bool: ph, int: pos) =
	if pos == sum_height then pos
	else if ph[pos] != ph[pos+1] then pos
	else height(ph,pos+1)
	endif
	endif;

int: max_width_index = get_index(width,height,max_width,1,1);

%order encoding

constraint forall(i in NCIRCUITS)( %first column is always false, in order to help the overlapping constraint over the leftmost block
	not(px[i,0])
);

constraint forall(i in NCIRCUITS)( %same here
 not(py[i,0])   
);

%order constraints

constraint forall(i in NCIRCUITS, e in 0..plate_width-width[i]-1)(
	not(px[i,e]) \/ px[i,e+1]
);

constraint forall(i in NCIRCUITS, f in 0..sum_height-height[i]-1)(
 not(py[i,f]) \/ py[i,f+1]
);

%the e and f in which the i-th block overlaps the maximum width and height must be true

constraint forall(i in NCIRCUITS, e in plate_width-width[i]..plate_width)(
	px[i,e]
);

constraint forall(i in NCIRCUITS, f in sum_height-height[i]..sum_height)(
	py[i,f]
);

%no overlapping

constraint forall(i in NCIRCUITS, j in i+1..N)( %block i must be either left, right, down, above the block j
	lr[i,j] \/ lr[j,i] \/ ud[i,j] \/ ud[j,i]
);

constraint forall(i in NCIRCUITS, j in i+1..N, e in 0..plate_width-width[i])(
	%if i is to the left of j, and if e is before i-th starting point, then e + the width of i must be before the starting point of j
	not(lr[i,j]) \/ px[i,e] \/ not(px[j,e+width[i]])
);

constraint forall(i in NCIRCUITS, j in i+1..N, f in 0..sum_height-height[j])(
	%same here
	not(ud[j,i]) \/ py[j,f] \/ not(py[i,f+height[j]])
);

constraint forall(i in NCIRCUITS, j in i+1..N, e in 0..plate_width-width[j])(
	%same here
	not(lr[j,i]) \/ px[j,e] \/ not(px[i,e+width[j]])
);

constraint forall(i in NCIRCUITS, j in i+1..N, f in 0..sum_height-height[i])(
	%same here
	not(ud[i,j]) \/ py[i,f] \/ not(py[j,f+height[i]]) 
);

%order constraint

constraint forall (o in max_height..sum_height-1)(
	not(ph[o]) \/ ph[o+1]
);

%if o is above all the blocks, then o - the height of i must be above i's starting point

constraint forall (o in max_height+1..sum_height-1, i in NCIRCUITS)(
	not(ph[o]) \/ py[i,o-height[i]]
);


var int: final_height = height(ph,max_height); %find position in which ph[o] switches from false to true (height that contains each block)

solve minimize final_height;

%output ["height=", show(final_height),"\n"];
