# Packing solver

In this repository you can find some solutions to the **packing problem**. The first model is in standard **CSP** written in *Minizinc*. We also defined **SAT** and **SMT** models, providing *Minizinc* and *Python Z3* solutions each. <br>
In order to write the models, we took inspiration from [A SAT-based Method for Solving the Two-dimensional Strip Packing Problem](http://ceur-ws.org/Vol-451/paper16soh.pdf) by Takehide Soh, Katsumi Inoue, Naoyuki Tamura, Mutsunori Banbara and Hidetomo Nabeshima.<br>
In order to execute the models implemented in *MiniZinc*, it is sufficient to pass as data file an instance which is in the format of the ones contained in the folder *instances_dzn*. Or, instead of defining a new instance, you could simply use the ones that are present inside the folder.<br>
On the other hand, the Python implementations based on the *Z3* library require that the folder *instances* is located at the same level as the scripts. In fact, each Python script accesses the folder and extracts the info about each instance and saves them inside a dictionary. This dictionary is then accessed in the code to specify on which instance the solver should operate. Here is the code: 
```python
w, n, plates = extract_data(get_instance(path, files_dict["ins-1"]))
```
The previously mentioned dictionary that contains the info about all the instances is named *files_dict* and its keys are the instance files' names. So, in order to execute the solver on the specific instance *ins-1*, for example, one has to simply change this line of code and replace *ins-1* with *ins-2* itself. Like this:
```python
w, n, plates = extract_data(get_instance(path, files_dict["ins-2"]))
```
