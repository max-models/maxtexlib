import argparse
import glob
import importlib.resources
import os
import shutil
import subprocess

import yaml

import maxtexlib
from maxtexlib.config import Config


def list_python_files(directory):
    """List all Python files in a given directory."""
    return [f for f in os.listdir(directory) if f.endswith(".py")]


def run_python_files(directory):
    """Run all Python files in the given directory with python3."""
    python_files = list_python_files(directory)
    for file in python_files:
        file_path = os.path.join(directory, file)
        print(f"Running {file_path}...")
        subprocess.run(["python3", file_path], check=True, cwd=directory)


def copy_template_files(sources, destination, yes=False):
    print(sources)
    for source in glob.glob(str(sources)):
        if os.path.exists(destination) and not yes:
            response = (
                input(f"File '{destination}' already exists. Overwrite? (Y/n): ")
                .strip()
                .lower()
            )
            if response not in ("y", "yes", ""):
                print("Operation canceled.")
                return
        shutil.copy(str(source), destination)


def setup_template(project_name, config, yes=False):
    """Copy main.tex from package templates to project directory, asking for confirmation if it exists."""

    # Paths
    project_path = config.get_path_project(project_name)
    main_tex_path = os.path.join(project_path, "main.tex")
    makefile_path = os.path.join(project_path, "makefile")
    path_figures = os.path.join(project_path, "figures")
    path_texfiles = os.path.join(project_path, "tex")

    # Create project directory
    os.makedirs(project_path, exist_ok=True)
    os.makedirs(path_figures, exist_ok=True)
    os.makedirs(path_texfiles, exist_ok=True)

    # Create main.tex
    source_path = importlib.resources.files("maxtexlib.templates").joinpath("main.tex")
    copy_template_files(sources=source_path, destination=main_tex_path, yes=yes)
    config.set_path_texfile(project_name, main_tex_path)

    # Create makefile
    source_path = importlib.resources.files("maxtexlib.templates").joinpath("makefile")
    copy_template_files(sources=source_path, destination=makefile_path, yes=yes)
    # config.set_path_makefile(project_name, makefile_path)

    # Copy figures/
    source_path = importlib.resources.files("maxtexlib.templates").joinpath(
        "figures/*.py"
    )
    copy_template_files(sources=source_path, destination=path_figures, yes=yes)
    config.set_path_figures(project_name, path_figures)

    # Copy tex/
    source_path = importlib.resources.files("maxtexlib.templates").joinpath("tex/*.tex")
    copy_template_files(sources=source_path, destination=path_texfiles, yes=yes)

    print(f"Template created in {project_path}")
    print(f"Config for project: {config.projects[project_name]}")

    config.save()


def main():

    config = Config.load()
    parser = argparse.ArgumentParser(description="LaTeX project builder")

    parser.add_argument(
        "-n", "--new", dest="NEW_PROJECT", type=str, help="Generate new LaTeX project"
    )

    parser.add_argument("-pr", "--project", dest="PROJECT", type=str, help="")

    parser.add_argument(
        "-p", "--path", dest="PATH", type=str, help="Set path to LaTeX project"
    )

    parser.add_argument(
        "--generate-figures",
        action="store_true",
        help="Generate figures for the LaTeX project",
    )

    parser.add_argument(
        "--figdir", type=str, help="Set the directory for storing figures"
    )
    parser.add_argument(
        "--texfile", type=str, help="Set the path for the main .tex file"
    )

    parser.add_argument(
        "--compile", action="store_true", help="Compile the LaTeX project"
    )

    parser.add_argument(
        "--generate-project-template",
        dest="GENERATE_TEMPLATE",
        action="store_true",
        help="Generate a project template",
    )

    parser.add_argument("-d", "--delete", action="store_true", help="Delete project")

    parser.add_argument(
        "-y", "--yes", action="store_true", help="Answer yes when asked"
    )

    args = parser.parse_args()

    PROJECT_NAME = None
    if args.NEW_PROJECT:
        PROJECT_NAME = args.NEW_PROJECT
        config.add_project(PROJECT_NAME)
        config.save()
    elif args.PROJECT:
        PROJECT_NAME = args.PROJECT

    if PROJECT_NAME is not None:
        if args.figdir:
            config.set_path_figures(PROJECT_NAME, args.figdir)
            config.save()
        if args.texfile:
            config.set_path_texfile(PROJECT_NAME, args.texfile)
            config.save()
        if args.PATH:
            config.set_path_project(PROJECT_NAME, args.PATH)
            config.save()

        if args.GENERATE_TEMPLATE:
            setup_template(PROJECT_NAME, config, args.yes)
        if args.generate_figures:
            print("Generating figures for the LaTeX project...")
            FIGURE_DIR = config.get_path_figures(PROJECT_NAME)
            if FIGURE_DIR:
                print(f"Generating figures in {FIGURE_DIR}")
                run_python_files(FIGURE_DIR)
            else:
                print("No figure directory set.")

        if args.compile:
            TEX_PATH = config.get_path_texfile(PROJECT_NAME)
            if TEX_PATH:
                subprocess.run(
                    ["latexmk", "-pdf", TEX_PATH],
                    check=True,
                    cwd=config.get_path_project(PROJECT_NAME),
                )
                print(f"Compiled document saved to: {TEX_PATH.replace('.tex', '.pdf')}")
            else:
                print("No tex path set")

        if args.delete:
            config.delete_project(PROJECT_NAME)
            config.save()


if __name__ == "__main__":
    main()
