# 2D-Brillouin-zone-algorithm
To compute and draw 2D Brillouin zones in several seconds

Install all libraries required.

__Note__: Installing CGAL-bindings could be tricky as the official one is unavailable for now. Please see my instruction here: https://github.com/Hui606/Install-CGAL-Bindings-for-python-and-java

To run the algorithm,

1. Input parameters required in input.py
    * Direction: it is the direction that the program follows to increase the number of unit cells
    * Points: they are the points in the unit cell
    * Range: it determines the number of unit cells in the result of the algorithm
    * Start & Stop:  users use them to extract the zones they want to observe

2. Run tracking_layer.py in terminals