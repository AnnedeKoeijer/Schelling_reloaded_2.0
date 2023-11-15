import mesa.space
from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from numpy import random
from statistics import mean
from plots import model_plots

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

    ''' Below step is completely changed compared to the other/old models (NEW) '''
    def step(self):
        average_parcel_income = self.model.parcel_values[self.pos]

        #If own income is higher than average income of current parcel
        if self.income > average_parcel_income:
            #print(f'this is the income: {self.income}')
            old_location = self.pos

            parcel_list = []

            if self.type == 0:
                #Look for parcels where they have on average a higher income than own income
                for key, value in self.model.parcel_values.items():
                    #print(f'this is the value: {value}')
                    if value > self.income or value ==0:
                        parcel_list.append(key)

            else:
                # Look for parcels where they have on average a lower income than own income
                for key, value in self.model.parcel_values.items():
                    # print(f'this is the value: {value}')
                    if value < self.income:
                        parcel_list.append(key)

            #If there is a 'wealthier' parcel, move to a randomly chosen one
            if len(parcel_list) != 0:
                new_location = self.model.random.choice(parcel_list)
                self.model.grid.move_agent(self, new_location)

        else:
            None

class Schelling(Model):
    """
    Model class for the Schelling segregation model.
    """

    def __init__(self, height=20, width=20, density=0.8, minority_pc=0.2):

        self.total_satisfaction_index = 0 # o indice total de agentes satisfeitos
        self.blue_satisfaction_index  = 0 # o indice de agentes azuis satisfeitos
        self.red_satisfaction_index   = 0 # o indice de agentes vermelhos satisfeitos
        self.total_blue_agents_count  = 0 # o total de agentes azuis
        self.total_red_agents_count   = 0 # o total de agentes vermelhos
        self.happy_blue_agents_count  = 0 # o numero de agentes azuis felizes
        self.happy_red_agents_count   = 0 # o numero de agentes vermelhos felizes

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
                "happy": "happy",
                "total_satisfaction_index": lambda m: self.total_satisfaction_index,
                "blue_satisfaction_index": lambda m: self.blue_satisfaction_index,
                "red_satisfaction_index": lambda m: self.red_satisfaction_index,
                "Segregated": get_segregation
            }, agent_reporters=
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )

        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)

        # The agent type is allocated using random instead of perfectly mixed (NEW)
        number_agents = round(self.width * self.height * self.density)
        agent_types_list =[]
        for number in range(0,number_agents):
            if self.random.random() < self.minority_pc:
                agent_type = 1  # Blue agents
            else:
                agent_type = 0  # Red agents
            agent_types_list.append(agent_type)

        # Placing the agents on the grid (every cell has 10 agents)
        for cell in self.grid.coord_iter():
            x = cell[1][0]
            y = cell[1][1]
            if self.random.random() < self.density:
                for i in range(0, 10):
                    agent_type = random.choice(agent_types_list)
                    if agent_type == 1:
                        agent = SchellingAgent((x, y, i), (x, y), self, agent_type,
                                               random.normal(loc=40, scale=5))  # Adding income distribution
                    else:
                        agent = SchellingAgent((x, y, i), (x, y), self, agent_type, random.normal(loc=100, scale=10))
                    self.grid.place_agent(agent=agent, pos=(x, y))
                    self.schedule.add(agent)

        self.running = True
        self.datacollector.collect(self)


    def step(self):
        """
        Run one step of the model. Update the average income in a parcel (NEW)
        """
        #Updating dictonary where (x,y) are the keys and the parcel's average income the value
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

                parcel_value = mean(income_list)
                self.parcel_values[(x,y)] = parcel_value

        #print(self.parcel_values)


        # calculates the blue and red satisfaction index
        self.blue_satisfaction_index = float(self.happy_blue_agents_count / max(self.total_blue_agents_count, 1))
        self.red_satisfaction_index  = float(self.happy_red_agents_count / max(self.total_red_agents_count, 1))
        # calculates the total satisfaction index
        total_agents = self.total_blue_agents_count + self.total_red_agents_count
        happy_agents = self.happy_blue_agents_count + self.happy_red_agents_count
        self.total_satisfaction_index = float(happy_agents / total_agents)


        self.happy = 0  # Reset counter of happy agents
        self.happy_blue_agents_count = 0
        self.happy_red_agents_count = 0

        #Make heatmap for number agents across the grid for this step
        model_plots(self)

        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        if self.happy == self.schedule.get_agent_count():
            self.running = False


#function to analyse the level of segregation
def get_segregation(model):
    '''
    Find the % of agents that only have neighbors of their same type.
    '''
    segregated_agents = 0
    for agent in model.schedule.agents:
        segregated = True
        for neighbor in model.grid.iter_neighbors(agent.pos, moore=True):
            if neighbor.type != agent.type:
                segregated = False
                break
        if segregated:
            segregated_agents += 1
    return segregated_agents / model.schedule.get_agent_count()




