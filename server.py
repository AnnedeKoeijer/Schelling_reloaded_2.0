from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import Slider

from model import Schelling


class HappyElement(TextElement):
    """
    Display a text count of how many happy agents there are.
    """

    def __init__(self):
        pass

    def render(self, model):
        return "Happy agents: " + str(model.happy)

class Agent_NumberElement(TextElement):
    """
        Display a text count of how many agents there are in the map.
    """

    def __init__(self):
        pass

    def render(self, model):
        return "Number agents: " + str(model.schedule.get_agent_count())

class IndexElement(TextElement):
    """
    Display a text index of the index of happy agents.
    """

    def __init__(self):
        pass

    def render(self, model):
        return "Index of satisfaction: " + str(round(model.total_satisfaction_index, 2))


def schelling_draw(agent):
    """
    Portrayal Method for canvas
    """
    if agent is None:
        return
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}

    if agent.type == 0:
        portrayal["Color"] = ["#FF0000", "#FF9999"]
        portrayal["stroke_color"] = "#00FF00"
    else:
        portrayal["Color"] = ["#0000FF", "#9999FF"]
        portrayal["stroke_color"] = "#000000"
    return portrayal

map_height = 30
map_width = 30

happy_element = HappyElement()
agent_number_element = Agent_NumberElement()
index_element = IndexElement()
canvas_element = CanvasGrid(schelling_draw, map_width, map_height, 500, 500)
happy_chart = ChartModule([
    {"Label": "happy", "Color": "Black"},
])
index_chart = ChartModule([
    {"Label": "total_satisfaction_index", "Color": "Green"},
    {"Label": "red_satisfaction_index", "Color": "Red"},
    {"Label": "blue_satisfaction_index", "Color": "Blue"},
])

model_params = {
    "height": map_height,
    "width": map_width,
    "density": Slider("Agent density", 0.8, 0.01, 1.0, 0.01),
    "minority_pc": Slider(
        "Fraction minority", 0.3, 0.00, 1.0, 0.01
    )
}

server = ModularServer(
    Schelling, [canvas_element,  agent_number_element, happy_element, happy_chart, index_element, index_chart], "Schelling", model_params
)
