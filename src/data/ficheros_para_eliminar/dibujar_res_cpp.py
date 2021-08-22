
from src.files_management import Parser
import matplotlib.pyplot as plt


current_parser = Parser('src/dataset/res.txt')
epsilon_error, data = current_parser.extract_data()
STARTING_POINTS = list(data)
FIGURE = plt.figure()
AXES = FIGURE.add_subplot()
AXES.scatter([point.x for point in STARTING_POINTS], [point.y for point in STARTING_POINTS], color='k',
         marker='x')
plt.show()
