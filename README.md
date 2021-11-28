# PyGoL
Python implementation of Conway's Game of Life

Using the Arcade framework: https://api.arcade.academy/en/latest/examples/conway_alpha.html#conway-alpha

Instead of iterating through every cell and its neighbors to determine the next state of the cell (alive or dead), I'm using Numpy and offset copies of a 2D bit array to get the number of live neighbors.
 
Video:

[![](http://img.youtube.com/vi/hi34mNl3XEU/0.jpg)](https://www.youtube.com/watch?v=hi34mNl3XEU "")
