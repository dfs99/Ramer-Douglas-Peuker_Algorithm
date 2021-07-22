import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
# lw: linewidth
line, = ax.plot([], [], lw=2)


# pinta la función inicial
def init_func():
    x = np.linspace(0, 10 * np.pi, 100)
    y = np.sin(x)
    # ax.clear()
    ax.plot(x, y, 'go-')
    line.set_data(x, y)
    return line,


def animate(i):
    z = random.randint(0, 75)
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    b = [-1, 0, 1, 0, -1, 0, 1, 0, -1, 0]
    x = np.linspace(0, 10 * np.pi, z)
    y = np.sin(x)
    # ax.clear()
    # ax.plot(x, y, 'go')
    line.set_data(x, y)
    line.set_color('red')
    line.set_marker('o')

    return line,

# nº de veces se actualiza el gráfico.
# poner la profundidad del arbol de busqueda y pasar en cada frame los ptos a dibujar.
#con la funcion animate.
depth = 1


ani = animation.FuncAnimation(fig, animate, init_func=init_func, frames=depth, interval=100, repeat=False, blit=True)

plt.show()
