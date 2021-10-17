include "diffn.mzn";

int: width;
int: num_of_circuits;
set of int: NCIRCUITS = 1..num_of_circuits;
array[NCIRCUITS,1..2] of int: size;

int: sum_height = sum(i in NCIRCUITS)(size[i,2]);
int: max_height = max(i in NCIRCUITS)(size[i,2]);

array[NCIRCUITS,NCIRCUITS] of var bool: lr;
array[NCIRCUITS,NCIRCUITS] of var bool: ud;
array[NCIRCUITS,0..width] of var bool: px;
array[NCIRCUITS,0..sum_height] of var bool: py;
array[max_height..sum_height] of var bool: ph;

function var int: height(array[max_height..sum_height] of var bool: ph, int: pos) =
	if pos == sum_height then pos
	else if ph[pos] != ph[pos+1] then pos
	else height(ph,pos+1)
	endif
	endif;

%order encoding

constraint forall(i in NCIRCUITS)(
	not(px[i,0])
);

constraint forall(i in NCIRCUITS)(
        not(py[i,0])   
);

constraint forall(i in NCIRCUITS, e in 0..width-size[i,1]-1)(
	not(px[i,e]) \/ px[i,e+1]
);

constraint forall(i in NCIRCUITS, e in width-size[i,1]..width)(
	px[i,e]
);

constraint forall(i in NCIRCUITS, f in 0..sum_height-size[i,2]-1)(
	not(py[i,f]) \/ py[i,f+1]
);

constraint forall(i in NCIRCUITS, f in sum_height-size[i,2]..sum_height)(
	py[i,f]
);


%no overlapping

constraint forall(i in NCIRCUITS, j in i+1..num_of_circuits)(
	lr[i,j] \/ lr[j,i] \/ ud[i,j] \/ ud[j,i]
);

constraint forall(i in NCIRCUITS, j in i+1..num_of_circuits, e in 0..width-size[i,1])(
	not(lr[i,j]) \/ px[i,e] \/ not(px[j,e+size[i,1]])
);

constraint forall(i in NCIRCUITS, j in i+1..num_of_circuits, f in 0..sum_height-size[j,2])(
	not(ud[j,i]) \/ py[j,f] \/ not(py[i,f+size[j,2]])
);

constraint forall(i in NCIRCUITS, j in i+1..num_of_circuits, e in 0..width-size[j,1])(
	not(lr[j,i]) \/ px[j,e] \/ not(px[i,e+size[j,1]])
);

constraint forall(i in NCIRCUITS, j in i+1..num_of_circuits, f in 0..sum_height-size[i,2])(
	not(ud[i,j]) \/ py[i,f] \/ not(py[j,f+size[i,2]]) 
);


constraint forall (o in max_height..sum_height-1)(
	not(ph[o]) \/ ph[o+1]
);

constraint forall (o in max_height+1..sum_height-1, i in NCIRCUITS)(
	not(ph[o]) \/ py[i,o-size[i,2]]
);

var int: final_height = height(ph,max_height);

solve minimize final_height;

%output["height= ", show(final_height), "\n"];
