from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from name_that_color.name_that_color import ntc


def main():
    colors = ntc().names  # initialize class to produce color data-frame from text lists

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.scatter3D(colors['r'], colors['g'], colors['b'], c=colors['hex_code'])
    ax.set_xlabel('r')
    ax.set_ylabel('g')
    ax.set_zlabel('b')
    plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.scatter3D(colors['hsl_x'], colors['hsl_y'], colors['l'], c=colors['hex_code'])
    ax.set_xlabel('hsl_x')
    ax.set_ylabel('hsl_y')
    ax.set_zlabel('l')
    plt.show()


if __name__ == '__main__':
    main()
