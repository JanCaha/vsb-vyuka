# soubor funkcí používaných napříč skripty a ukázkami

import typing
from pathlib import Path

import arcpy


def setup_env(path: typing.Optional[str] = None) -> None:
    """Nastavení workspace pro práci."""
    file_path = Path(__file__)
    base_path = file_path.parent / "data"
    if path is None:
        arcpy.env.workspace = base_path
    else:
        workspace_path = f"{base_path}/{path}"
        arcpy.env.workspace = workspace_path
        exist = arcpy.Exists(arcpy.env.workspace)
        if not exist:
            raise ValueError(f"Workspace path {workspace_path} does not exist!")
    arcpy.env.overwriteOutput = True


def is_projected(crs: arcpy.SpatialReference) -> bool:
    return crs.type == "Projected"
