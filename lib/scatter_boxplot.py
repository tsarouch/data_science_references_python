from matplotlib import pyplot as plt
import numpy as np
import pylab
from matplotlib import gridspec
import ipdb


"""
Inspired from the "Introduction to Statistical Learning" of James et al.
where we see a scatter plot of two variables and  the corresponding boxplots.

It can be particularily useful for a binary classification case where we have to pass
the target binary variable too.
"""



def add_box_plot(ax, vec1, vec2, colors, xlabel, labels):
    """ Add of the box plot of individual variables so that we can
    see how the separation looks like in 1 dim
    """
    box = ax.boxplot([vec1, vec2], notch=True, patch_artist=True)
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    #pylab.xticks(range(1, len(colors)+1), labels, rotation=0)
    ax.set_ylabel(xlabel)
    ax.set_xticklabels(labels)
    
    
def add_scatter_plot(ax, a_x, a_y, b_x, b_y,
                     xlabel, ylabel,
                     a_marker, b_marker, a_color, b_color):
    """ Add of the scatter plot of the variables so that we can
    see how the separation looks like in 2 dimentions
    """
    if len(a_x) > len(b_x): 
        ax.scatter(a_x, a_y, marker=a_marker, color=a_color, alpha=0.7)
        ax.scatter(b_x, b_y, marker=b_marker, color=b_color, alpha=0.7)
    else:
        ax.scatter(b_x, b_y, marker=b_marker, color=b_color, alpha=0.7)
        ax.scatter(a_x, a_y, marker=a_marker, color=a_color, alpha=0.7)

    ax.grid(True)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def add_title(fig, title, explanation, a_marker, b_marker):
    """ Constructs and adds the title
    """
    fig.suptitle(title, fontsize=14)
    if explanation:
        title += '\n ' + a_marker + ': ' + explanation + ' True'
        title += '\n ' + b_marker + ': ' + explanation + ' False'

        
def finlalize_plot(filename):
    """ Saves of plots the final plot
    """
    if filename:
        plt.savefig(filename, bbox_inches='tight')
    else:
        plt.show()
    plt.clf()
    plt.cla()
    plt.close()


def get_fig_objects(boxplots):
    """ Returns the necessary figure objects
    """
    fig = None
    axes= []
    if boxplots:
        fig = plt.figure(figsize=(20, 10))
        gs = gridspec.GridSpec(1, 3, width_ratios=[2, 1, 1])
        axes.append(plt.subplot(gs[0]))
        axes.append(plt.subplot(gs[1]))
        axes.append(plt.subplot(gs[2]))
    else:
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        axes.append(ax)

    return fig, axes


def plot_2d_data(df, col_x, col_y, col_cat, filename=None,
                 boxplots=True,
                 title='', xlabel='', ylabel='', explanation=None,
                 a_marker='o', b_marker='x',
                 a_color='blue', b_color='red'):
    """ Plot of scatter plot based on
    :param df: the DataFrame that holds the data
        - col_x, var x
        - col_y, var y
        - col_cat , takes a bool value to decalre the category it belongs
    :param explanation: explanation what means the class a, b.
        - e.g. explanation='smoker case'
        - will be displayed under title
    """
    # get data properly
    a_df = df[df[col_cat] == True]
    a_x = a_df[col_x].values
    a_y = a_df[col_y].values

    b_df = df[df[col_cat] == False]
    b_x = b_df[col_x].values
    b_y = b_df[col_y].values

    if xlabel=='': 
        xlabel = col_x
    if ylabel=='':
        ylabel = col_y
        
    fig, axes = get_fig_objects(boxplots)

    # The main scatter plot
    add_scatter_plot(axes[0], a_x, a_y, b_x, b_y, xlabel, ylabel,
                     a_marker, b_marker, a_color, b_color)

    # Boxplots if asked
    if boxplots:
        colors = [a_color, b_color]
        labels = ['no', 'yes']
        add_box_plot(axes[1], a_y, b_y, colors, ylabel, labels)
        add_box_plot(axes[2], a_x, b_x, colors, xlabel, labels)

    # Title
    add_title(fig, title, explanation, a_marker, b_marker)

    # close plot
    finlalize_plot(filename)