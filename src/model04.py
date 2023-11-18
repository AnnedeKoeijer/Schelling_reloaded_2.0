import mesa.space
from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from numpy import random
from statistics import mean
from statistics import median
import numpy as np
# from plots import model_plots
from scipy.stats import skewnorm
from scipy.stats import uniform

class SchellingAgent(Agent):
    """
    Schelling segregation agent
    """

    def __init__(self, unique_id, pos, model, income):
        """
        Create a new Schelling agent.

        Args:
           unique_id: Unique identifier for the agent.
           x, y: Agent initial location.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.income = income
        self.unique_id = unique_id

    def step(self):
        '''
        This step is completely changed compared to the other/old models. It defines when and how an agent will move (changed 15/11)
        '''

        lower_bound, median_parcel_income, upper_bound = self.model.parcel_values[self.pos]
        difference_average = self.income - median_parcel_income

        #If own income is higher than the upper bound or lower than the lower bound of the cells income distribution
        if (self.income > upper_bound) or (self.income < lower_bound):

            parcel_list = []

            #Append cells whos median income is closer to the agents distribution or cells that are empty
            for key, value in self.model.parcel_values.items():
                if value == 0:      #If the cell is empty
                    parcel_list.append(key)
                else:
                    #If on right side of the median, agent is able to move to a cell to a cell where it is closer to the median than before,
                    # disregarding left or right to that median
                    # If on right side of the median, agent is able to move to a cell to a cell where it is closer to the median than before,
                    # restricting to only left side of the that median (NEW)
                    if difference_average >0:
                        if abs(self.income - value[1]) < difference_average:
                            parcel_list.append(key)
                    else:
                        if (self.income - value[1]) < 0 and (self.income - value[1]) > difference_average:
                            parcel_list.append(key)


            #If possible, move to a rnadom new location that is closer to agents own income
            if len(parcel_list) != 0:
                new_location = self.model.random.choice(parcel_list)
                values_new = self.model.parcel_values[new_location]
                #print(f'This is my difference {difference_average} and income {self.income}, and I am going to this new difference {values_new}')
                #print(new_location)
                self.model.grid.move_agent(self, new_location)

        else:
            None

class Schelling(Model):
    """
    Model class for the Schelling segregation model [Changed 15/11].
    """

    def __init__(self, height=20, width=20, density=0.8, income_distribution_type='right'):
        self.height = height
        self.width = width
        self.density = density
        self.income_distribution_type = income_distribution_type

        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, torus=False)

        self.parcel_values = {}

        self.datacollector = DataCollector(model_reporters=
            {
                "happy": "happy",
            }, agent_reporters=
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )

        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)
        #Placing the agents on the grid (every cell has 10 agents)
        for cell in self.grid.coord_iter():
            x = cell[1][0]
            y = cell[1][1]
            if self.random.random() < self.density:
                for i in range(0,10):
                    if self.income_distribution_type =='right':
                        agent = SchellingAgent((x,y,i), (x, y), self, skewnorm.rvs(10, loc=40, scale=25, size=1)[0]) #Adding income distribution
                    elif self.income_distribution_type =='left':
                        agent = SchellingAgent((x, y, i), (x, y), self, skewnorm.rvs(-5, loc=120, scale=25, size=1)[0])
                    elif self.income_distribution_type =='normal':
                        agent = SchellingAgent((x, y, i), (x, y), self, random.normal(loc=80, scale=15))
                    elif self.income_distribution_type =='uniform':
                        agent = SchellingAgent((x, y, i), (x, y), self, uniform.rvs(loc=30, scale=100))
                    else:
                        print("ERROR no correct income distribution type defined!!")
                    self.grid.place_agent(agent =agent, pos=(x, y))
                    self.schedule.add(agent)


        self.running = True
        self.datacollector.collect(self)


    def step(self):
        """
        Run one step of the model. Update the average income in a parcel (changed 04/11)
        """
        #Updating dictonary where (x,y) coordinates are the keys and the parcel's average income the value
        for cell in self.grid.coord_iter():
            income_list =[]

            list_agents = cell[0]
            x = cell[1][0]
            y = cell[1][1]

            if self.grid.is_cell_empty((x, y)):
                self.parcel_values[(x,y)] = 0

            else:
                for agent in list_agents:
                    income_list += [agent.income]

                for neighbor in self.grid.iter_neighbors(pos=(x,y),moore=True):
                    income_list.append(neighbor.income)

                parcel_value_median = median(income_list)
                parcel_value_std = np.std(income_list)
                #print(f'median: {parcel_value_median}')
                #print(f'std: {parcel_value_std}')
                lower_bound = parcel_value_median - parcel_value_std
                upper_bound = parcel_value_median + parcel_value_std
                self.parcel_values[(x,y)] = (lower_bound ,parcel_value_median, upper_bound)

        #print(self.parcel_values)

        # Reset counter of happy agents
        self.happy = 0

        #Make heatmap for number agents across the grid for this step
        print(self.schedule.steps)
        # model_plots(self)

        #Next step
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)






