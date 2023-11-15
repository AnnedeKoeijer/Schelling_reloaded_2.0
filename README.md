# SchellingSegregation

This directory consists out of multiple models, who all have the same file setup.
In model.py the model is set up. To run the model and analyse is, use the analysis.ipynb file. The run.py file can also be used to run the model while visualising it (in a webbrowser). However, for these models, the visualisation does not add much/any value.
The plots.py file includes the code for the function that is responsible for creating distribution plots for every time step.

Within each model file there is file called 'modelrun_images', in which per run the plots per timestep are saved. **Important** to note is that these images are not deleted when a new modelrun is started.
Therefore, when a new run is started which has fewer runtime than the model before, the folder might contain images from the previous run (as they are not overwritten)

The models are slightly different form each other. Below, first the baseline workings each model has is explained, followed by the unique workings per model. The main difference between the models is when and how the agents move: The 'rule of the game'.

## Models ##
### Baseline model workings ###

* agents: each agent has 
    * a class (A/B), with the proportion of 70/30 of total agents (allocation per cell drawn from global distribution) 
    * an income (drawn from a distribution A or B, where A > B)
* checkerboard: e.g. 10x10=100 cells 
* (initially) 20% empty cells, and 80% occupied cells
* the cells can hold any number of agents (in this case, from 0 to 800)
* (initially) each of the occupied cells has 10 agents, randomly selected from the entirety of agents (without regards to their income or group)
* (Torus turned off)

**Important notes**:

- Distribution A is for now fixed at a mean of 100, with a std of 10.
- Distribution B is for now fixed at a mean of 40, with a std of 5
- The average income on of a parcel is updated at the start of every tick, and thus **not** every time an agent moves. This can be adjusted. 

### Model 1 ##

* “system nudge” (or “rule of the game?”): each agent seeks to “up their game” = if their income is higher than the mean income of the cell, they move want to move.
An agents move to a randomly selected other cell where their income is **lower** than the mean income of that cell or to an empty cell. B Agents move to a randomly selected other cell where their income is **higher** than the mean.
* note: we don’t care about boundary conditions in this one because “neighbourhood” is defined as all people IN your cell, not NEXT to it 

### Model 2 ###

*  “rule of the game?”: If an agent's income is more than 1 std away from the **mean** income of the agent's **cell**, it moves to a new cell for which the agent's income is closer to the mean than its previous location (using the income of all agents residing in that cell to create an income distribution)
* note: we don’t care about boundary conditions in this one because “neighbourhood” is defined as all people IN your cell, not NEXT to it 

### Model 3 ###

*  “rule of the game?”: If an agent's income is more than 1 std away from the **median** income of the agent's **neighborhood**, it moves to a new cell for which the agent's income is closer to the neighborhood's **median** than its previous location (using the income of all agents residing in that cell and the surrounding 8 cells to create an income distribution)
* note: Here we **do** care about boundary conditions, as neighborhood is defined as all the agents in your cell **and** next to it. (so the median income is the median of all the agents in the neighborhood together)  

### Model 4 (Differentiates from baseline model) [New 14/11] ###

* Similar to model 3, however
* In this model we step away from different types of agents and use 'one type of agent' whose income is drawn from the same distribution.
* The income distribution can be skewed to the left or right, normal, or uniform
* Change/extend "rule of the game": Agent who are on the right side of the neighborhoods income median (difference is positive) and who desire to move, will move to a cell where there income is closer to the median, in terms of absolute difference. 
Agent who are on the left side of the median (difference is negative) and desire to move, will move to a cell where there income is closer **but still below** the median. Therefore, the agents who are 'richer' are able to move to neighborhoods where they, again, will be richer, or to neighborhoods where they are 'poorer'. The 'poorer' agents can only move to neighborhoods where the, again, are the 'poorer'.

<hr>

## Setting up a conda environment ##

To set up a conda environment for the Jupyter notebook: 
* open the command line interface (Terminal on macOS/Anaconda Prompt on Windows)
* navigate to the main project folder
* run in terminal:
```
conda env create -f schelling-env.yml
conda activate schell
```
* next, to run the Jupyter notebook, make sure to activate the `schell` environment first 
* to run the `.py` script (visulization in the browser), use 
```
python3 <filename.py>
```