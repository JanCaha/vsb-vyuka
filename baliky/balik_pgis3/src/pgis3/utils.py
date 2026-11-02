import os
import re
import typing
import unicodedata
from pathlib import Path

import arcpy

MAIN_DIR = Path(os.environ.get("PGIS3_DATA_DIR", r"C:/Projekty"))


def workspace_path(sub_folder: typing.Optional[str] = None) -> Path:
    """Vrátí cestu ke složce s daty pro předmět PGIS3."""
    base_path = MAIN_DIR / "PGIS3" / "data"
    if sub_folder is None:
        return base_path
    return base_path / sub_folder


def setup_env(sub_folder: typing.Optional[str] = None) -> None:
    """Nastavení workspace pro práci."""
    workspace = workspace_path(sub_folder)

    exist = arcpy.Exists(arcpy.env.workspace)
    if not exist:
        raise ValueError(f"Workspace path {workspace} does not exist!")

    arcpy.env.workspace = workspace.as_posix()
    arcpy.env.overwriteOutput = True


def is_projected(crs: arcpy.SpatialReference) -> bool:
    """Vrátí True pro projektované souřadnicové systémy."""
    return crs.type.lower() == "projected"


def normalize_name(name: str) -> str:
    """Převede název do podoby vhodné pro ArcGIS vrstvy a datové sady.

    Odstraní diakritiku, nahradí mezery a speciální znaky podtržítky a vrátí
    jméno v lowercase. Pokud po úpravě zůstane prázdný řetězec, vrátí default
    `dataset`.
    """

    text = unicodedata.normalize("NFKD", str(name))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = text.strip("_")
    return text
