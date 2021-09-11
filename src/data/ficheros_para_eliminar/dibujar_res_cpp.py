
from src.files_management import Parser
import matplotlib.pyplot as plt


#current_parser = Parser('src/dataset/res.txt')
#epsilon_error, data = current_parser.extract_data()
#STARTING_POINTS = list(data)
#FIGURE = plt.figure()
#AXES = FIGURE.add_subplot()
#AXES.scatter([point.x for point in STARTING_POINTS], [point.y for point in STARTING_POINTS], color='k',
#         marker='x')
#plt.show()

l = [1, 2, 3, 4, 5]
end = len(l)-1
start = 0
print("total len", len(l))
print("end index", end)
print("start index", start)
print(l[0:end+1])

def order_y(p):
    return p[1]
def order_x(p):
    return p[0]

l = [(11,60), (81,79), (12,40), (81,80), (81,81), (81,78), (81,82), (12,90)]
l.sort(key=order_y)
print(l)
k = [(11,60), (81,79), (12,40), (81,80), (81,81), (81,78), (81,82), (12,90)]
k.sort(key=order_x)
print(k)
z = [(11,60), (81,79), (12,40), (81,80), (81,81), (81,78), (81,82), (12,90)]
z.sort(key=order_y)
z.sort(key=order_x)
print(z)
