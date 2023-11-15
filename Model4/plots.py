import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
import seaborn as sns

def model_plots(model):
    # Increase the size of the figure
    plt.figure(figsize=(13, 4))  # Adjust width and height as needed

    model_income = []
    model_density = []

    # Code for the first plot (Heatmap: Number of agents)
    agent_counts = np.zeros((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter():
        cell_content = cell[0]
        x = cell[1][0]
        y = cell[1][1]
        agent_count = len(cell_content)
        agent_counts[x][y] = agent_count

    # Create the first subplot
    plt.subplot(1, 3, 1)  # 1 row, 3 columns, first plot
    plt.imshow(agent_counts, cmap="Greys_r", interpolation='nearest',
               extent=(0, model.grid.width, 0, model.grid.height), vmin=0, vmax=40)
    plt.title(f'Step {model.schedule.steps}: Number of agents across the grid')
    plt.colorbar(shrink=0.9)

    # Set grid lines to be every 1 unit
    plt.xticks(np.arange(0, model.grid.width + 1, 1))
    plt.yticks(np.arange(0, model.grid.height + 1, 1))

    # Add grid
    plt.grid(True)

    # Code for the second plot (Heatmap: Income distribution across grid)
    agent_counts = np.zeros((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter():
        list_income = []
        cell_content = cell[0]
        x = cell[1][0]
        y = cell[1][1]
        density = len(cell_content)
        model_density.append(density)
        if len(cell_content) != 0:  # If there are agents on the cell
            for agent in cell_content:
                list_income.append(agent.income)
            mean_income = mean(list_income)
        else:
            mean_income = 0
        model_income.append(mean_income)
        agent_counts[x][y] = mean_income

    # Create the second subplot
    plt.subplot(1, 3, 2)  # 1 row, 3 columns, second plot
    plt.imshow(agent_counts, cmap="GnBu", interpolation='nearest',
               extent=(0, model.grid.width, 0, model.grid.height), vmin=0, vmax=120)
    plt.title(f'Step {model.schedule.steps}: Mean income per parcel across the grid')
    plt.colorbar(shrink=0.9)

    # Set grid lines to be every 1 unit
    plt.xticks(np.arange(0, model.grid.width + 1, 1))
    plt.yticks(np.arange(0, model.grid.height + 1, 1))

    # Add grid
    plt.grid(True)

    # Create the third subplot (Scatterplot: Income and density)
    plt.subplot(1, 3, 3)  # 1 row, 3 columns, third plot
    sns.scatterplot(x=model_density, y=model_income)
    plt.xlabel('Number agents on a cell')
    plt.ylabel('Average income')
    plt.title(f'Step {model.schedule.steps}: Distribution average income per density')

    # Set x-axis and y-axis limits
    plt.xlim(0, 40)  # Set x-axis limit from 0 to 35
    plt.ylim(0, 130)  # Set y-axis limit from 0 to 140

    # Adjust the layout to prevent overlap
    plt.tight_layout()

    #Save the model to the right file
    if model.schedule.steps < 10:
        plt.savefig(f'../Model4/modelrun_images/step00{model.schedule.steps}.png')
    else:
        plt.savefig(f'../Model4/modelrun_images/step0{model.schedule.steps}.png')

    # Show the plots
    plt.show()