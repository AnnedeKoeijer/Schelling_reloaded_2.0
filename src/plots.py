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

# ### to add later: code for plots with normalized boundaries

# # find absolute max values for density and income

# # max_income (if income stays the same across the entire model)
# max_income = max([item for sublist in df.loc[0,"agent_incomes"].values() for item in sublist])
# max_income = np.round(math.ceil(max_income/10))*10 # rounding up to nearest upper multiple of 10

# # max agent density per cell
# max_count = df.apply(lambda x: max(x.agent_counts.values()), axis = 1).max()
# max_count = np.round(math.ceil(max_count/10))*10 # rounding up to nearest upper multiple of

# # make folder and plots at each step

# os.makedirs("../results/model04/", exist_ok = True)

# for mystep in range(total_steps):

#     zfill_step = "{:03d}".format(mystep)
#     print(zfill_step)

#     fig, ax = plt.subplots(1,3, figsize = (30,10))

#     vals_counts_incomes = {}

#     # plot agent numbers
#     i = 0
#     vals_counts = np.zeros((model.width, model.height))
#     for k, v in df.loc[mystep, "agent_counts"].items():
#         vals_counts_incomes[k] = {}
#         vals_counts_incomes[k]["count"] = v
#         vals_counts[k]=v
#     im = ax[i].imshow(
#         vals_counts,
#         vmin = 0,
#         vmax = max_count,
#         cmap = "Reds",
#         )
#     ax[i].set_title("Agent counts")
#     ax[i].set_axis_off()
#     plt.colorbar(im, shrink = 0.7)

#     # plot agent mean incomes
#     i = 1
#     vals_incomes = np.zeros((model.width, model.height))
#     for k, v in df.loc[mystep, "agent_incomes"].items():
#         vals_counts_incomes[k]["income"] = v
#         if v:
#             vals_incomes[k]=statistics.median(v)
#     ax[i].set_title("Income medians")
#     im = ax[i].imshow(
#         vals_incomes,
#         vmin = 0, 
#         vmax = max_income,
#         cmap = "Greens"
#         )
#     ax[i].set_axis_off()
#     plt.colorbar(im, shrink = 0.7)

#     # plot agent counts vs. median incomes
#     i = 2
#     ax[i].scatter(
#         x = [v["count"] for v in vals_counts_incomes.values()],
#         y = [statistics.median(v["income"]) if v["income"] else 0 for v in vals_counts_incomes.values()],
#         s = 5,
#         color = "black"
#     )
#     ax[i].set_title("Agent count vs. median income")
#     ax[i].set_xlim([0,max_count])
#     ax[i].set_xlabel("Agent counts")
#     ax[i].set_ylim([0,max_income])
#     ax[i].set_ylabel("Agent incomes")
#     plt.title(zfill_step)
#     fig.savefig(f"../results/model04/{zfill_step}.png")

#     plt.close()

# # make video
# fps = 1
# img_folder_name = "../results/model04/"
# images = sorted([img for img in os.listdir(img_folder_name) if img.endswith(".png")])
# video_name = "../results/model04/video.mp4"
# frame = cv2.imread(os.path.join(img_folder_name, images[0]))
# height, width, layers = frame.shape
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# video = cv2.VideoWriter(video_name, fourcc, fps, (width,height))
# for image in images:
#     video.write(cv2.imread(os.path.join(img_folder_name, image)))
# cv2.destroyAllWindows()
# video.release()