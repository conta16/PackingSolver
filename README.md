# Packing solver

In this repository you can find some solutions to the **packing problem**. The first model is in standard **CSP** written in *Minizinc*. We also defined **SAT** and **SMT** models, providing *Minizinc* and *Python Z3* solutions each. <br>
In order to write the models, we took inspiration from [A SAT-based Method for Solving the Two-dimensional Strip Packing Problem](http://ceur-ws.org/Vol-451/paper16soh.pdf) by Takehide Soh, Katsumi Inoue, Naoyuki Tamura, Mutsunori Banbara and Hidetomo Nabeshima

##Dependencies

- Minizinc (version 2.5.5)
- Python 3.9.7 and following libraries:
- - numpy (1.20.3)
- - matplotlib (3.4.3)

The code has not been tested on other versions, so it may need some changes depending on the software you are using

## How to use Minizinc SAT model

Run, from your terminal, the command

```python3 ./minizinc/launcher.py [/path/to/file.dzn]```

The script will automatically launch the *Minizinc* solver and show its output in *Matplotlib*