import matplotlib.pyplot as plt
import numpy as np
from src.data import Point

m1, b1 = -2.0, 15.0
m2, b2 = 0.5, 1.5
m3, b3 = 1.0, -1.0
print(m1*m2)
print(m1*m3)

x = np.linspace(4, 7, 5)
FIGURE = plt.figure()
AXES = FIGURE.add_subplot()
AXES.plot(x, x*m1+b1)
AXES.plot(x, x*m2+b2)
AXES.plot(x, x*m3+b3)

AXES.plot([7, 4], [1, 7], 'ko')
AXES.plot([5.4], [4.2], 'go')
AXES.plot([5], [4], 'bo')

STARTING_POINTS = [Point(1.0, 1.0), Point(2.0, 3.0), Point(4.0, 7.0),
                   Point(5.0, 4.0), Point(6.0, 5.0), Point(7.0, 1.0)]
AXES.plot([point.x for point in STARTING_POINTS], [point.y for point in STARTING_POINTS], color='k', linestyle='dashed',
         marker='o', lw=1)
AXES.set_box_aspect(1)
plt.show()
