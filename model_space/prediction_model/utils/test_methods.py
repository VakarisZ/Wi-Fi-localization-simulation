from typing import List

import numpy as np
from matplotlib import pyplot as plt

from model_space.utils.point import Point


def interpolation(data):
    data = np.array([line.split() for line in data.split('\n')], dtype=float)

    x, y = data.T
    xd = np.diff(x)
    yd = np.diff(y)
    dist = np.sqrt(xd ** 2 + yd ** 2)
    u = np.cumsum(dist)
    u = np.hstack([[0], u])

    t = np.linspace(0, u.max(), 30)
    xn = np.interp(t, u, x)
    yn = np.interp(t, u, y)

    f = plt.figure()
    ax = f.add_subplot(111)
    ax.set_aspect('equal')
    ax.plot(x, y, 'o', alpha=0.3)
    ax.plot(xn, yn, 'ro', markersize=8)
    ax.set_xlim(0, 5)
    plt.show()


def history_interpolation(history: List[Point]):

    x = np.asarray([point.x for point in history])
    y = np.asarray([point.y for point in history])
    xd = np.diff(x)
    yd = np.diff(y)
    dist = np.sqrt(xd ** 2 + yd ** 2)
    u = np.cumsum(dist)
    u = np.hstack([[0], u])

    t = np.linspace(0, u.max(), len(history))
    xn = np.interp(t, u, x)
    yn = np.interp(t, u, y)

    f = plt.figure()
    ax = f.add_subplot()
    ax.plot(x, y, 'o', alpha=0.3)
    ax.plot(xn, yn, 'ro', markersize=8)
    plt.show()


if __name__ == "__main__":
    data = '''0.615   5.349
        0.615   5.413
        0.617   6.674
        0.617   6.616
        0.63    7.418
        0.642   7.809
        0.648   8.04
        0.673   8.789
        0.695   9.45
        0.712   9.825
        0.734   10.265
        0.748   10.516
        0.764   10.782
        0.775   10.979
        0.783   11.1
        0.808   11.479
        0.849   11.951
        0.899   12.295
        0.951   12.537
        0.972   12.675
        1.038   12.937
        1.098   13.173
        1.162   13.464
        1.228   13.789
        1.294   14.126
        1.363   14.518
        1.441   14.969
        1.545   15.538
        1.64    16.071
        1.765   16.7
        1.904   17.484
        2.027   18.36
        2.123   19.235
        2.149   19.655
        2.172   20.096
        2.198   20.528
        2.221   20.945
        2.265   21.352
        2.312   21.76
        2.365   22.228
        2.401   22.836
        2.477   23.804'''

    interpolation(data)
    input("Finished")
