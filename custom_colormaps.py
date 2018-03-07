"""
NAME
    Custom Colormaps for Matplotlib
PURPOSE
    This program shows how to implement make_cmap which is a function that
    generates a colorbar
PROGRAMMER(S)
    Chris Slocum
REVISION HISTORY
    20130411 -- Initial version created
    20140313 -- Small changes made and code posted online
    20140320 -- Added the ability to set the position of each color
    20150724 -- Attempted to make this more Pythonic
    20180307 -- Changed license to BSD 3-clause
"""
import numpy as np


def create_colormap(colors, position=None, bit=False, reverse=False, name='custom_colormap'):
    """
    returns a linear custom colormap

    Parameters
    ----------
    colors : array-like
        contain RGB values. The RGB values may either be in 8-bit [0 to 255]
        or arithmetic [0 to 1] (default).
        Arrange your tuples so that the first color is the lowest value for the
        colorbar and the last is the highest.
    position : array like
        contains values from 0 to 1 to dictate the location of each color.
    bit : Boolean
        8-bit [0 to 255] (in which bit must be set to
        True when called) or arithmetic [0 to 1] (default)
    reverse : Boolean
        If you want to flip the scheme
    name : string
        name of the scheme if you plan to save it

    Returns
    -------
    cmap : matplotlib.colors.LinearSegmentedColormap
        cmap with equally spaced colors
    """
    from matplotlib.colors import LinearSegmentedColormap
    if not isinstance(colors, np.ndarray):
        colors = np.array(colors, dtype='f')
    if reverse:
        colors = colors[::-1]
    if position is not None and not isinstance(position, np.ndarray):
        position = np.array(position)
    elif position is None:
        position = np.linspace(0, 1, colors.shape[0])
    else:
        if position.size != colors.shape[0]:
            raise ValueError("position length must be the same as colors")
        elif not np.isclose(position[0], 0) and not np.isclose(position[-1], 1):
            raise ValueError("position must start with 0 and end with 1")
    if bit:
        colors[:] = [tuple(map(lambda x: x / 255., color)) for color in colors]
    cdict = {'red':[], 'green':[], 'blue':[]}
    for pos, color in zip(position, colors):
        cdict['red'].append((pos, color[0], color[0]))
        cdict['green'].append((pos, color[1], color[1]))
        cdict['blue'].append((pos, color[2], color[2]))
    return LinearSegmentedColormap(name, cdict, 256)


if __name__ == "__main__":
    # An example of how to use make_cmap
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(311)
    # Create a list of RGB tuples
    colors = [(255, 0, 0), (255, 255, 0), (255, 255, 255), (0, 157, 0), (0, 0, 255)] # This example uses the 8-bit RGB
    # Call the function make_cmap which returns your colormap
    my_cmap = create_colormap(colors, bit=True)
    # Use your colormap
    plt.pcolor(np.random.rand(25, 50), cmap=my_cmap)
    plt.colorbar()
    ax = fig.add_subplot(312)
    colors = [(1, 1, 1), (0.5, 0, 0)] # This example uses the arithmetic RGB
    # If you are only going to use your colormap once you can
    # take out a step.
    plt.pcolor(np.random.rand(25, 50), cmap=create_colormap(colors))
    plt.colorbar()

    ax = fig.add_subplot(313)
    colors = [(0.4, 0.2, 0.0), (1, 1, 1), (0, 0.3, 0.4)]
    # Create an array or list of positions from 0 to 1.
    position = [0, 0.3, 1]
    plt.pcolor(np.random.rand(25, 50), cmap=create_colormap(colors, position=position))
    plt.colorbar()
    plt.savefig("example_custom_colormap.png")
    plt.show()
