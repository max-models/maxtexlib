import json
import os
from dataclasses import asdict, dataclass, field
from typing import Dict

import maxtexlib

LIBPATH = os.path.abspath(maxtexlib.__path__[0])
PATH_CONFIG = os.path.join(LIBPATH, "config.json")


@dataclass
class LatexProject:
    path_project: str = None
    path_figures: str = None
    path_texfile: str = None


@dataclass
class Config:
    projects: Dict[str, LatexProject] = field(default_factory=dict)

    @classmethod
    def load(cls, file_path=PATH_CONFIG) -> "Config":
        """Load configuration from a JSON file. If the file doesn't exist, create an empty one."""
        if not os.path.exists(file_path):
            # Create an empty JSON file
            with open(file_path, "w") as file:
                json.dump({"projects": {}}, file, indent=4)
            return cls()  # Return a default empty config

        with open(file_path, "r") as file:
            data = json.load(file)
            projects = {
                name: LatexProject(**proj)
                for name, proj in data.get("projects", {}).items()
            }
            return cls(projects=projects)

    def save(self, file_path=PATH_CONFIG) -> None:
        """Save the configuration to a JSON file."""
        with open(file_path, "w") as file:
            json.dump(
                {
                    "projects": {
                        name: asdict(proj) for name, proj in self.projects.items()
                    }
                },
                file,
                indent=4,
            )

    def reset(self) -> None:
        """Reset the configuration by clearing all projects."""
        self.projects.clear()

    def add_project(self, name: str) -> None:
        """Add a new LaTeX project with a unique name."""
        if name in self.projects:
            raise ValueError(f"Project '{name}' already exists.")
        self.projects[name] = LatexProject()  # Add new empty project

    def delete_project(self, name: str) -> None:
        """Delete a new LaTeX project with a unique name."""
        if not name in self.projects:
            raise ValueError(f"Project '{name}' doesn't exist.")
        del self.projects[name]

    def get_path_project(self, project) -> str:
        """Get path_project to one of the projects."""
        if project not in self.projects:
            raise ValueError(f"Project '{project}' doesn't exist.")
        return self.projects[project].path_project

    def get_path_figures(self, project) -> str:
        """Get path_figures to one of the projects."""
        if project not in self.projects:
            raise ValueError(f"Project '{project}' doesn't exist.")
        return self.projects[project].path_figures

    def get_path_texfile(self, project) -> str:
        """Get path_texfile to one of the projects."""
        if project not in self.projects:
            raise ValueError(f"Project '{project}' doesn't exist.")
        return self.projects[project].path_texfile

    def set_path_project(self, project, path_project) -> None:
        """Set path_figures to one of the projects."""
        if project not in self.projects:
            raise ValueError(f"Project '{project}' doesn't exist.")
        self.projects[project].path_project = os.path.abspath(path_project)

    def set_path_figures(self, project, path_figures) -> None:
        """Set path_figures to one of the projects."""
        if project not in self.projects:
            raise ValueError(f"Project '{project}' doesn't exist.")
        self.projects[project].path_figures = os.path.abspath(path_figures)

    def set_path_texfile(self, project, path_texfile) -> None:
        """Set path_texfile to one of the projects."""
        if project not in self.projects:
            raise ValueError(f"Project '{project}' doesn't exist.")
        self.projects[project].path_texfile = os.path.abspath(path_texfile)


if __name__ == "__main__":
    # Load config
    config = Config.load()

    # Modify config
    config.add_project("proj2")
    print(config.projects["proj2"])
