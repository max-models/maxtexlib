# generate_figures.py

import os

import matplotlib.pyplot as plt
import maxplotlib.canvas.canvas as canvas
import numpy as np


def plot_figure1(filename="sample_plot"):

    # Sample data
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    c = canvas.Canvas(width=2000, ratio=0.5)
    sp = c.add_subplot(
        grid=True,
        xlabel="(x - 10) * 0.1",
        ylabel="10y",
        yscale=10,
        xshift=-10,
        xscale=0.1,
    )
    sp.add_line([0, 1, 2, 3], [0, 1, 4, 9], label="Line 1")
    sp.add_line(
        [0, 1, 2, 3], [0, 2, 3, 4], linestyle="dashed", color="red", label="Line 2"
    )
    # c.plot()

    c.savefig(filename=filename)


def main():
    plot_figure1()


if __name__ == "__main__":
    main()
