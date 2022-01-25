# Packing solver

In this repository you can find some solutions to the **packing problem**. We defined a **SAT** encoding, providing *Minizinc* and *Python Z3* solutions each. <br>
In order to write the models, we took inspiration from [A SAT-based Method for Solving the Two-dimensional Strip Packing Problem](http://ceur-ws.org/Vol-451/paper16soh.pdf) by Takehide Soh, Katsumi Inoue, Naoyuki Tamura, Mutsunori Banbara and Hidetomo Nabeshima.

## Dependencies

- Minizinc (version 2.5.5)
- Python 3.9.7 and following libraries:
- - numpy (1.20.3)
- - matplotlib (3.4.3)
- - z3-solver (4.8.13.0)

The code has not been tested on other versions, so it may need some changes depending on the software you are using

## How to use Minizinc SAT model

Run, from your terminal, the command

```python3 ./minizinc/launcher.py [/path/to/file.mzn] [/path/to/file.dzn]```

The script will automatically launch the *Minizinc* solver and show its output in *Matplotlib*.<br>
For *Minizinc* it is also available a program which gives the solution considering a possible rotation (swap between width and height dimensions) of the circuits.<br>
Among the ``.mzn`` files in ``/src``, the best performing ones are ``SATpacking_sym_search.mzn`` and ``SATpacking_rotation_sym_search.mzn``.

## How to use Python Z3 SAT model

Run, from your terminal, the command

```python3 ./z3/SATpacking.py [/path/to/file.xml]```

The script will automatically launch the *Python Z3* solver and show its output in *Matplotlib*.<br>
In *Python Z3*, rotation is not implemented, but computation is improved by applying the same constraints specified in *Minizinc*.