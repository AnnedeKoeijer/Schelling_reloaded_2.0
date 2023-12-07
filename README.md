# SchellingSegregation

> Insert project description

<!-- The plots.py file includes the code for the function that is responsible for creating distribution plots for every time step Within each model file there is file called 'modelrun_images', in which per run the plots per timestep are saved. **Important** to note is that these images are not deleted when a new modelrun is started. Therefore, when a new run is started which has fewer runtime than the model before, the folder might contain images from the previous run (as they are not overwritten) -->

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
* to run the `.py` script (visulization in the browser), use 
```
python3 <filename.py>
```

## Running a model

To run and analyze theoutcomes of a model, create a Jupyter notebook in the `/notebooks/` folder. Then, indicate which model you want to run when importing the Schelling class. For example, to run model01, import like so:
```python
from src.model01 import Schelling
``` 

The different models are explained in detail [here](/DOCS.md).

## References

Original Schelling model implementation based on (@gustavo-tomas)[@gustavo-tomas]: https://github.com/gustavo-tomas/SchellingSegregation 