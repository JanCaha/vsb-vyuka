from __future__ import annotations

import inspect
import pathlib
import typing
import warnings

CACHE_DIR = pathlib.Path.home() / ".cache" / "balicekpgis2"
EXTRACT_DIR = CACHE_DIR / "extracted"
BASE_DIR = None


if not EXTRACT_DIR.exists():
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)


def cache_file(filename: str) -> pathlib.Path:
    """Vytvoří cestu k souboru v cache adresáři."""
    return CACHE_DIR / filename


def extracted_folder(filename: str) -> pathlib.Path:
    """Vytvoří cestu k extrahovanému souboru."""
    folder = EXTRACT_DIR / filename
    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)
    return folder


class PathManager:
    """Správce základní cesty (singleton)."""

    _instance: typing.Optional[PathManager] = None  # Singleton instance
    _base_dir: typing.Optional[pathlib.Path] = None

    def __new__(cls, *args, **kwargs):
        """Zajišťuje, že existuje pouze jedna instance třídy PathManager."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Získání základního adresáře podle aktuálního skriptu, který je spuštěn, když se třída poprvé inicializuje
            this_directory = pathlib.Path(__file__).parent
            for frame in inspect.stack():
                # cesta k aktuálnímu frame stacku
                target_path = pathlib.Path(frame.filename)
                # pokud je aktuální frame stack v jiném adresáři než tento skript -> není součástí balíčku
                if not (this_directory in target_path.parents or this_directory == target_path):
                    cls._base_dir = target_path.parent
                    break

        return cls._instance

    def set_base_path(self, base_dir: pathlib.Path) -> None:
        """Nastaví základní adresář pro skript."""
        self._base_dir = base_dir
        if not self._base_dir.exists():
            self._base_dir.mkdir(parents=True, exist_ok=True)

    def get_base_path(self) -> pathlib.Path:
        """Vrací základní adresář."""
        if self._base_dir is None:
            raise ValueError("Base path has not been set.")
        return self._base_dir

    def base_data_path(self) -> pathlib.Path:
        """Vrací cestu ke složce s daty jako objekt Path."""
        if self._base_dir is None:
            raise ValueError("Base path has not been set.")
        return self._base_dir / "data"

    def data_path(self, filename: str) -> pathlib.Path:
        """Vrací cestu k souboru s daným názvem souboru jako objekt Path. Pokud soubor neexistuje, vyvolá chybu."""
        file = self.base_data_path() / filename
        if not file.exists():
            raise ValueError(f"File {file.as_posix()} does not exist.")
        return file

    def base_save_data_path(self) -> pathlib.Path:
        """Vrací cestu ke složce pro uložení dat jako objekt Path. Pokud složka neexistuje, vytvoří ji."""
        path = self.base_data_path() / "saved"
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        return path

    def save_data_path(self, filename: str, delete_if_exist: bool = False) -> pathlib.Path:
        """Vrací cestu k souboru pro uložení dat jako objekt Path. Pokud soubor existuje, vyvolá varování a pokud je nastaveno delete_if_exist na True, soubor smaže."""
        path = self.base_save_data_path() / filename
        if path.exists():
            warnings.warn(f"File {path.as_posix()} exists.")
            if delete_if_exist:
                warnings.warn("File was deleted!")
                path.unlink()
        return path
