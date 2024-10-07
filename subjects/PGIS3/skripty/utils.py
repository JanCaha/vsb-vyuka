# soubor funkcí používaných napříč skripty a ukázkami

import typing

import arcpy


def setup_env(path: typing.Optional[str] = None) -> None:
    """Nastavení workspace pro práci."""
    base_path = "Projekty/PGIS3/data"
    if path is None:
        arcpy.env.workspace = base_path
    else:
        workspace_path = f"{base_path}/{path}"
        arcpy.env.workspace = workspace_path
        exist = arcpy.Exists(arcpy.env.workspace)
        if not exist:
            raise ValueError(f"Workspace path {workspace_path} does not exist!")
    arcpy.env.overwriteOutput = True
