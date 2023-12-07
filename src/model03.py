from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from numpy import random
from statistics import median
import numpy as np
from src.plots import model_plots

class SchellingAgent(Agent):
    """
    Schelling segregation agent
    """

    def __init__(self, unique_id, pos, model, agent_type, income):
        """
        Create a new Schelling agent.

        Args:
           unique_id: Unique identifier for the agent.
           x, y: Agent initial location.
           agent_type: Indicator for the agent's type (minority=1, majority=0)
        """
        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type
        self.income = income
        self.unique_id = unique_id

    def step(self):
        '''
        This step defines when and how an agent will move (changed 04/11)
        '''

        lower_bound, median_parcel_income, upper_bound = self.model.parcel_values[self.pos]
        difference_average = abs(self.income-median_parcel_income)

        #If own income is higher than the upper bound or lower than the lower bound of the cells income distribution
        if (self.income > upper_bound) or (self.income < lower_bound):

            parcel_list = []

            #Append cells whos median income is closer to the agents distribution or cells that are empty
            for key, value in self.model.parcel_values.items():
                if value == 0:      #If the cell is empty
                    parcel_list.append(key)

                else:
                    if abs(self.income - value[1]) < difference_average:
                        parcel_list.append(key)

            #If possible, move to a rnadom new location that is closer to agents own income
            if len(parcel_list) != 0:
                new_location = self.model.random.choice(parcel_list)
                self.model.grid.move_agent(self, new_location)

        else:
            None

class Schelling(Model):
    """
    Model class for the Schelling segregation model [Changed 13/11].
    """

    def __init__(self, height=20, width=20, density=0.8, minority_pc=0.2):
        self.height = height
        self.width = width
        self.density = density
        self.minority_pc = minority_pc

        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, torus=False)

        self.parcel_values = {}

        self.happy = 0
        self.datacollector = DataCollector(model_reporters=
            {
            }, agent_reporters=
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )

        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)

        # The agent type is allocated using random instead of perfectly mixed (NEW)
        number_agents = round(self.width * self.height*10)
        agent_types_list =[]
        for number in range(0,number_agents):
            if self.random.random() < self.minority_pc:
                agent_type = 1  # Blue agents
            else:
                agent_type = 0  # Red agents
            agent_types_list.append(agent_type)


        #Placing the agents on the grid (every cell has 10 agents)
        for cell in self.grid.coord_iter():
            x = cell[1][0]
            y = cell[1][1]
            if self.random.random() < self.density:
                for i in range(0,10):
                    agent_type = random.choice(agent_types_list)
                    if agent_type == 1:
                        agent = SchellingAgent((x,y,i), (x, y), self, agent_type, random.normal(loc=40, scale=5)) #Adding income distribution
                    else:
                        agent = SchellingAgent((x,y,i) ,(x, y), self, agent_type, random.normal(loc=100, scale=10))
                    # Find the index of the first occurrence of '1'
                    index_of_one = agent_types_list.index(agent_type)
                    # Remove the first occurrence of '1'
                    agent_types_list.pop(index_of_one)
                    self.grid.place_agent(agent =agent, pos=(x, y))
                    self.schedule.add(agent)


        self.datacollector.collect(self)
        print('Model3')


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
                lower_bound = parcel_value_median - parcel_value_std
                upper_bound = parcel_value_median + parcel_value_std
                self.parcel_values[(x,y)] = (lower_bound ,parcel_value_median, upper_bound)


        #Make heatmap for number agents across the grid for this step
        print(self.schedule.steps)
        model_plots(self)

        #Next step
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)







