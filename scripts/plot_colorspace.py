import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from name_that_color.name_that_color import ntc


def main():
    ntc_object = ntc()

    # colors = ntc_object.names  # initialize class to produce color data-frame from text lists
    colors = pd.read_pickle('../colors_categorized.pkl').sample(5000)

    colors['category_code'] = colors['basic_name'].apply(ntc_object.shadergb)

    fig = plt.figure()

    ax1 = fig.add_subplot(2, 2, 1, projection="3d")
    ax1.scatter3D(colors['r'], colors['g'], colors['b'], c=colors['hex_code'])
    ax1.set_xlabel('r')
    ax1.set_ylabel('g')
    ax1.set_zlabel('b')

    ax2 = fig.add_subplot(2, 2, 2, projection="3d")
    ax2.scatter3D(colors['hsl_x'], colors['hsl_y'], colors['l'], c=colors['hex_code'])
    ax2.set_xlabel('hsl_x')
    ax2.set_ylabel('hsl_y')
    ax2.set_zlabel('l')

    ax3 = fig.add_subplot(2, 2, 3, projection="3d")
    ax3.scatter3D(colors['r'], colors['g'], colors['b'], c=colors['category_code'])
    ax3.set_xlabel('r')
    ax3.set_ylabel('g')
    ax3.set_zlabel('b')

    ax4 = fig.add_subplot(2, 2, 4, projection="3d")
    ax4.scatter3D(colors['hsl_x'], colors['hsl_y'], colors['l'], c=colors['category_code'])
    ax4.set_xlabel('hsl_x')
    ax4.set_ylabel('hsl_y')
    ax4.set_zlabel('l')

    plt.show()


if __name__ == '__main__':
    main()
