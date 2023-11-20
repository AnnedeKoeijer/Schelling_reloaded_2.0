# SchellingSegregation

> TO DO: explain the project main idea

## Repository structure

- `/notebooks/` contains an analysis in jupyter notebook for each of the models
- `/results/` contains results from model runs
- `/scripts/` contains python scripts to be run from terminal
- `/src/` contains python files to be imported (collection of functions) - one for each model, plus plotting a separate file for plotting functions

## Setting up a conda environment ##

To set up a conda environment for the Jupyter notebook: 
* open the command line interface (Terminal on macOS/Anaconda Prompt on Windows)
* navigate to the main project folder
* run in terminal:
```
conda env create -f schelling-env.yml
conda activate schell
pip install -e .
```
* next, to run the Jupyter notebook, make sure to activate the `schell` environment first 
<!-- * to run the `.py` script (visulization in the browser), use 
```
python3 <filename.py>
``` (commenting this one out because the browser visualization doesn't work for our models I think?) -->

## Running a model

To run and analyze theoutcomes of a model, create a Jupyter notebook in the `/notebooks/` folder. Then, indicate which model you want to run when importing the Schelling class. For example, to run model01, import like so:
```python
from src.model01 import Schelling
``` 

The different models are explained in detail [here](/docs/MODELS.md).