"""An example of how to use make_cmap."""
import matplotlib.pyplot as plt
import numpy as np
from custom_colormaps import create_colormap


fig = plt.figure()
ax = fig.add_subplot(411)
# Create a list of RGB tuples
colors = [(255, 0, 0), (255, 255, 0), (255, 255, 255), (0, 157, 0),
          (0, 0, 255)]    # This example uses the 8-bit RGB
# Call the function make_cmap which returns your colormap
my_cmap = create_colormap(colors)
# Use your colormap
plt.pcolor(np.random.rand(25, 50), cmap=my_cmap)
plt.colorbar()
ax = fig.add_subplot(412)
colors = [(1, 1, 1), (0.5, 0, 0)]    # This example uses the arithmetic RGB
# If you are only going to use your colormap once you can
# take out a step.
plt.pcolor(np.random.rand(25, 50), cmap=create_colormap(colors))
plt.colorbar()

ax = fig.add_subplot(413)
colors = [(0.4, 0.2, 0.0), (1, 1, 1), (0, 0.3, 0.4)]
# Create an array or list of positions from 0 to 1.
position = [0, 0.3, 1]
plt.pcolor(np.random.rand(25, 50),
           cmap=create_colormap(colors, position=position))
plt.colorbar()

ax = fig.add_subplot(414)
colors = ['blue', 'white', 'yellow', 'red']
plt.pcolor(np.random.rand(25, 50), cmap=create_colormap(colors))
plt.colorbar()
plt.savefig("example_custom_colormap.png")
plt.show()
