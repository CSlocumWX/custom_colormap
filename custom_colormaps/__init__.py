"""
Custom Colormaps for Matplotlib.


This program shows how to implement custom_colormap and
custom_breakpoint_colormap, which are functions that
generates a colormap based on user input.

Notes
-----
* 20130411 -- Initial version created
* 20140313 -- Small changes made and code posted online
* 20140320 -- Added the ability to set the position of each color
* 20150724 -- Attempted to make this more Pythonic
* 20180307 -- Changed license to BSD 3-clause
* 20240325 -- Added breakpoint colormap generator
"""
import ast
from typing import Optional, Union, Tuple
from numbers import Number
import numpy as np
import numpy.typing as npt
from matplotlib.colors import ColorConverter, LinearSegmentedColormap

__version__ = "2.0"
__author__ = "Chris Slocum"


def normalize(value: Union[Number, npt.ArrayLike],
              vmin: Optional[Number] = None,
              vmax: Optional[Number] = None) -> Union[Number, np.ndarray]:
    """
    Normalize value.

    Parameters
    ----------
    value : float or array-like
        The value(s) that need normalizing
    vmin : float, optional
        The minimum value for all values
    vmax : float, optional
        The maximum value for all values

    Returns
    -------
    value : float or array-like
        The normalized value(s)
    """
    if vmin is None or vmax is None:
        if not isinstance(value, (list, np.ndarray, np.generic)):
            raise ValueError("Either define vmin/vmax or make value array-like")
        vmin = np.min(value)
        vmax = np.max(value)
    norm = (value - vmin) / float(vmax - vmin)
    return norm


def convert_color(color: str) -> Tuple[Number, Number, Number]:
    """
    Convert color to RGB.

    Parameters
    ----------
    color : str or array-like
        Color representation

    Returns
    -------
    color : tuple
        RGB representation of color
    """
    # convert ndarray type to matplotlib RGB [0..1]
    if isinstance(color, (np.ndarray, np.generic)):
        if np.issubdtype(color.dtype, np.integer):
            color = color / 255.
        color = ColorConverter().to_rgb(color)
        return color
    if any(isinstance(elem, int) and elem > 1 for elem in color):
        color = tuple(elem / 255. for elem in color)
    # Convert start/end color to string, tuple, whatever matplotlib RGB [0..1].
    try:
        color = ColorConverter().to_rgb(str(color))
    except ValueError:
        # Allow for tuples as well as string representations
        color = ColorConverter().to_rgb(ast.literal_eval(str(color)))
    return color


def create_colormap(colors: npt.ArrayLike,
                    position: Optional[npt.ArrayLike] = None,
                    bit: bool = False,
                    reverse: bool = False,
                    name: str = 'custom_colormap') -> LinearSegmentedColormap:
    """
    Returns a linear custom colormap.

    Parameters
    ----------
    colors : array-like
        An array-like object of colors corresponding to each postion
        element. Colors can be defined as HEX code, color names, or RGB
        values. RGB data assumes data types are floats for [0..1] or
        integers for [0..255].
    position : array-like, optional
        A list of monotonic position values corresponding to each color.
        If None, linear spacing is assumed.
    bit : Boolean, default=False
        8-bit [0 to 255] (in which bit must be set to
        True when called) or arithmetic [0 to 1] (default)
        Note: script still checks RGB data.
    reverse : Boolean, default=False
        If you want to flip the colormap
    name : string, default='custom_colormap'
        Name of the colormap

    Returns
    -------
    cmap : matplotlib.colors.LinearSegmentedColormap
        matplotlib colormap instance
    """
    if reverse:
        colors = colors[::-1]
    if position is None:
        position = np.linspace(0, 1, len(colors))
    if len(position) != len(colors):
        raise ValueError("position length must be the same as colors")
    # get the max/min values from positions
    vmin = np.min(position)
    vmax = np.max(position)
    # check position order
    if np.isclose(position[0], vmax):
        colors = colors[::-1]
        position = position[::-1]

    if bit:
        colors = np.array(
            [tuple(map(lambda x: x / 255., color)) for color in colors])
    segmentdata = {'red': [], 'green': [], 'blue': []}
    for pos, color in zip(position, colors):
        x = normalize(pos, vmin, vmax)
        color = convert_color(color)
        segmentdata['red'].append((x, color[0], color[0]))
        segmentdata['green'].append((x, color[1], color[1]))
        segmentdata['blue'].append((x, color[2], color[2]))
    cmap = LinearSegmentedColormap(name, segmentdata)
    return cmap


def create_breakpoint_colormap(
        colors: npt.ArrayLike,
        position: Optional[npt.ArrayLike] = None,
        name: str = 'custom_breakpoint_colormap') -> LinearSegmentedColormap:
    """
    Create a LinearSegmentedColormap instance with breakpoints.

    Parameters
    ----------
    colors : array-like
        An array-like object of color pairs corresponding to each postion
        element. Colors can be defined as HEX code, color names, or RGB
        values. RGB data assumes data types are floats for [0..1] or
        integers for [0..255].
    position : array-like, optional
        A list of monotonic position start-stop pairs corresponding to each
        color pair. If None, linear spacing is assumed.
    name : str, optional
        Name of the colormap.

    Returns
    -------
    cmap : matplotlib.colors.LinearSegmentedColormap
        matplotlib colormap instance
    """
    # create position if None
    if position is None:
        position = np.empty((len(colors), 2))
        tmp = np.linspace(0, 1, len(colors) + 1)
        position[:, 0] = tmp[:-1]
        position[:, 1] = tmp[1:]
    if len(position) != len(colors):
        raise ValueError("position length must be the same as colors")
    if any(len(elem) != 2 for elem in position):
        raise ValueError("Each element in position must have a length of 2")
    if any(len(elem) != 2 for elem in colors):
        raise ValueError("Each element in colors must have a length of 2")
    # get the max/min values from position
    vmin = np.min(position)
    vmax = np.max(position)
    # check position order
    if np.isclose(position[0][0], vmax):
        raise ValueError("position must increase")
    # Note y0 in the first row and y1 in the last row are never used.
    y0 = [0, 0, 0]
    y1 = [1, 1, 1]
    # color dictionary for LinearSegmentedColormap
    segmentdata = {'red': [], 'green': [], 'blue': []}
    for pos, color in zip(position, colors):
        pos_start = pos[0]
        y1 = convert_color(color[0])
        x = normalize(pos_start, vmin, vmax)
        segmentdata['red'].append((x, y0[0], y1[0]))
        segmentdata['green'].append((x, y0[1], y1[1]))
        segmentdata['blue'].append((x, y0[2], y1[2]))
        # Update y0
        pos_stop = pos[1]
        y0 = convert_color(color[1])
    x = normalize(pos_stop, vmin, vmax)
    segmentdata['red'].append((x, y0[0], y1[0]))
    segmentdata['green'].append((x, y0[1], y1[1]))
    segmentdata['blue'].append((x, y0[2], y1[2]))
    cmap = LinearSegmentedColormap(name, segmentdata)
    return cmap
