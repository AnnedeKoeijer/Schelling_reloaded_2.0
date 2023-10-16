# SchellingSegregation

In model.py the model is setup. To run the model and analyse is, use the analysis.ipynb file. The run.py file can also be used to run the model while visualising it (in a webbrowser). However, for this baseline model, the visualisation does not add much/any value. The other files in this directory are not of importance (yet). 

### Baseline model workings ###

* agents: each agent has 
    * a class (A/B), with the proportion of 70/30 of total agents, and 
    * an income (drawn from a distribution A or B, where A > B)
* checkerboard: e.g. 10x10=100 cells 
* (initially) 20% empty cells, and 80% occupied cells
* the cells can hold any number of agents (in this case, from 0 to 800)
* (initially) each of the occupied cells has 10 agents, randomly selected from the entirety of agents (without regards to their income or group)
* “system nudge” (or “rule of the game?”): each agent seeks to “up their game” = if their income is higher than the mean income of the cell, they move to a randomly selected other cell where their income is lower than the mean income of that cell or to an empty cell
* note: we don’t care about boundary conditions in this one because “neighbourhood” is defined as all people IN your cell, not NEXT to it 

**Important notes**:

- Distribution A is for now fixed at a mean of 100, with a std of 10.
- Distribution B is for now fixed at a mean of 40, with a std of 5
- 
