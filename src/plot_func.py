import numpy as np
import matplotlib.pyplot as plt
import statistics

def plot_densities(model, densities):
    '''
    helper function used in combine_subplots
    input: a dict with key = cell index, value = number of agents
    output:
    '''
    pass

def plot_incomes(model, incomes):
    '''
    helper function used in combine_subplots
    input: a dict with key = cell index, value = list of incomes
    output:
    '''
    pass

def plot_densities_incomes(model, densities, incomes):
    '''
    helper function used in combine_subplots
    input: 
    - densities: a dict with key = cell index, value = number of agents
    - incomes: a dict with key = cell index, value = list of incomes
    '''


def combine_subplots(list_of_figs):
    '''
    combines several subplots into one, and adds title / description
    '''
    pass

# def model_plots(model):
#     # Increase the size of the figure
#     plt.figure(figsize=(13, 4))  # Adjust width and height as needed

#     model_income = []
#     model_density = []

#     # Code for the first plot
#     agent_counts = np.zeros((model.grid.width, model.grid.height))
#     for cell in model.grid.coord_iter():
#         cell_content = cell[0]
#         x = cell[1][0]
#         y = cell[1][1]
#         agent_count = len(cell_content)
#         agent_counts[x][y] = agent_count

#     # Create the first subplot
#     plt.subplot(1, 3, 1)  # 1 row, 2 columns, first plot
#     plt.imshow(agent_counts, cmap="Greys_r", interpolation='nearest',
#                extent=(0, model.grid.width, 0, model.grid.height))
#     plt.title('Number of agents across the grid')
#     plt.colorbar(shrink=0.9)

#     # Set grid lines to be every 1 unit
#     plt.xticks(np.arange(0, model.grid.width + 1, 1))
#     plt.yticks(np.arange(0, model.grid.height + 1, 1))

#     # Add grid
#     plt.grid(True)

#     # Code for the second plot
#     agent_counts = np.zeros((model.grid.width, model.grid.height))
#     for cell in model.grid.coord_iter():
#         list_income = []
#         cell_content = cell[0]
#         x = cell[1][0]
#         y = cell[1][1]
#         density = len(cell_content)
#         model_density.append(density)
#         if len(cell_content) != 0:  # If there are agents on the cell
#             for agent in cell_content:
#                 list_income.append(agent.income)
#             mean_income = mean(list_income)
#         else:
#             mean_income = 0
#         model_income.append(mean_income)
#         agent_counts[x][y] = mean_income

#     # Create the second subplot
#     plt.subplot(1, 3, 2)  # 1 row, 2 columns, second plot
#     plt.imshow(agent_counts, cmap="coolwarm", interpolation='nearest',
#                extent=(0, model.grid.width, 0, model.grid.height))
#     plt.title('Mean income per parcel across the grid')
#     plt.colorbar(shrink=0.9)

#     # Set grid lines to be every 1 unit
#     plt.xticks(np.arange(0, model.grid.width + 1, 1))
#     plt.yticks(np.arange(0, model.grid.height + 1, 1))

#     # Add grid
#     plt.grid(True)

#     # Create the third subplot
#     plt.subplot(1, 3, 3)  # 1 row, 3 columns, third plot
#     sns.scatterplot(x=model_density, y=model_income)
#     plt.xlabel('Number agents on a cell')
#     plt.ylabel('Average income')
#     plt.title('Distribution average income per density')

#     # Adjust the layout to prevent overlap
#     plt.tight_layout()

#     # Show the plots
#     plt.show()