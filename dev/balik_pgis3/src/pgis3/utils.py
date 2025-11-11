import typing
from pathlib import Path

import arcpy

MAIN_DIR = Path("C:/Projekty")


def setup_env(sub_folder: typing.Optional[str] = None) -> None:
    """Nastavení workspace pro práci."""
    if sub_folder is None:
        arcpy.env.workspace = MAIN_DIR / "PGIS3" / "data"
    else:
        workspace_path = MAIN_DIR / "PGIS3" / "data" / sub_folder
        arcpy.env.workspace = workspace_path
        exist = arcpy.Exists(arcpy.env.workspace)
        if not exist:
            raise ValueError(f"Workspace path {workspace_path} does not exist!")
    arcpy.env.overwriteOutput = True


def is_projected(crs: arcpy.SpatialReference) -> bool:
    return crs.type == "Projected"
