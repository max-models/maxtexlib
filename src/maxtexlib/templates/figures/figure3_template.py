import maxtikzlib.logo


def plot_figure2(filename="mtl_logo.pdf"):

    fig = maxtikzlib.logo.generate_logo()
    fig.compile_pdf(filename)


def main():
    plot_figure2()


if __name__ == "__main__":
    main()
