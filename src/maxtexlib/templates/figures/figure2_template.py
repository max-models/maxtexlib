# generate_figures.py

import os

import matplotlib.pyplot as plt
import numpy as np
from maxplotlib.logo.logo import tikz_logo


def plot_figure2(filename="mpl_logo.tex"):

    tikz_logo_canvas = tikz_logo()

    # print(c.subplots[0,0].generate_tikz())
    tikz_logo_canvas.savefig(filename)
    # c.savefig(filename=filename)
    # with open(filename, 'w') as f:
    #     f.write(script)


def main():
    plot_figure2()


if __name__ == "__main__":
    main()
