# Packing solver

In this repository you can find some solutions to the **packing problem**. We defined a standard **CSP** encoding, providing a *Minizinc* solution. <br>

## Dependencies

- Minizinc (version 2.5.5)
- Python 3.9.7 and following libraries:
- - numpy (1.20.3)
- - matplotlib (3.4.3)

The code has not been tested on other versions, so it may need some changes depending on the software you are using

## How to use Minizinc CSP model

Run, from your terminal, the command

```python3 ./minizinc/launcher.py [/path/to/file.mzn] [/path/to/file.dzn]```

The script will automatically launch the *Minizinc* solver and show its output in *Matplotlib*.<br>
The ```no_global_constraint.mzn``` file contains no optimization and it is the slowest.<br>
The ```global_constraint.mzn``` file contains global constraints and implied constraints, while ```global_constraint_sym.mzn``` gives a faster solution by also applying symmetry breaking.
```global_constraint_sym_search.mzn``` also applies annotated search. <br>
The ```global_constraint_search_rotation.mzn``` file implements a solution which takes care of possible rotations (swapping between width and height) of each circuit.


