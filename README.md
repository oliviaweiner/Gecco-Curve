# Gecco-Curve

This code provides functionalities to produce the first three iterations of the Gecco curve coordinates. The aim of this project is to use the gecco curve coordinates to model a conic cavity for Professor Chao Lin Kuo. The gecco_curve.py file contains the functions that map the shape of the gecco curve. It uses the coordinates of a circles to build and output the coordinates of the gecco curves, which it then maps using matplotlib.  The outside_curve.py file contains functions that use the gecco curve created in gecco_curve.py to produce coordinates for the outside and inside wall of our cavity. Lastly, testing.py provides a series of tests to assess the functionality of the functions in the previous two files. To our knowledge a function to produce coordinates for a gecco_curve has not been done previously.

The following third party libraries were used:
- math
- matplotlib
- numpy
- argparse
- unittest
