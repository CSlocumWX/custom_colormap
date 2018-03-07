# Custom colormaps

A small routine to generate custom colormaps for [Matplotlib](https://matplotlib.org/).
The function allows you to create a list of tuples with 8-bit (0 to 255) or arithmetic (0.0 to 1.0)
RGB values to create linear colormaps by taking your list and converting it into a dictionary
that can work with [LinearSegmentedColormap](https://matplotlib.org/api/_as_gen/matplotlib.colors.LinearSegmentedColormap.html).

## Example
```python
from custom_colormaps import create_colormap
import numpy as np
import matplotlib.pyplot as plt
fig = plt.figure()
colors = [(255, 0, 0), (255, 255, 0), (255, 255, 255), (0, 157, 0), (0, 0, 255)] # This example uses the 8-bit RGB
my_cmap = create_colormap(colors, bit=True)
plt.pcolor(np.random.rand(25, 50), cmap=my_cmap)
plt.colorbar()
plt.show()
```

Original post and tutorial is located at [Custom Colormaps](http://schubert.atmos.colostate.edu/~cslocum/custom_cmap.html).
