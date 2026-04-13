from __future__ import annotations

import inspect
import pathlib
import typing
import warnings

# Standardní adresáře pro cacheování
CACHE_DIR = pathlib.Path.home() / ".cache" / "balicekpgis2"
EXTRACT_DIR = CACHE_DIR / "extracted"
BASE_DIR: typing.Optional[pathlib.Path] = None


if not EXTRACT_DIR.exists():
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)


def cache_file(filename: str) -> pathlib.Path:
    """Vytvoří cestu k souboru v cache adresáři.

    Parametry:
        filename: Název souboru.

    Returns:
        Cesta k souboru v cache adresáři.
    """
    return CACHE_DIR / filename


def extracted_folder(foldername: str) -> pathlib.Path:
    """Vytvoří cestu k extrahovanému adresáři.

    Parametry:
        foldername: Název adresáře.

    Returns:
        Cesta k adresáři, který je vytvořen, pokud neexistuje.
    """
    folder = EXTRACT_DIR / foldername
    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)
    return folder


class PathManager:
    """Správce základní cesty (singleton).

    Pomáhá spravovat cesty v kontextu spuštěného skriptu. Automaticky detekuje
    základní adresář na základě zásobníku volání.
    """

    _instance: typing.Optional[PathManager] = None
    _base_dir: typing.Optional[pathlib.Path] = None

    def __new__(cls) -> PathManager:
        """Zajišťuje, že existuje pouze jedna instance třídy PathManager."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Získání základního adresáře podle aktuálního skriptu
            this_directory = pathlib.Path(__file__).parent
            for frame in inspect.stack():
                target_path = pathlib.Path(frame.filename)
                # Pokud je aktuální frame stack mimo balíček, použije se jako base_dir
                if not (this_directory in target_path.parents or this_directory == target_path):
                    cls._base_dir = target_path.parent
                    break

        return cls._instance

    def set_base_path(self, base_dir: pathlib.Path) -> None:
        """Nastaví základní adresář pro skript.

        Parametry:
            base_dir: Cesta k novému základnímu adresáři.
        """
        self._base_dir = base_dir
        if not self._base_dir.exists():
            self._base_dir.mkdir(parents=True, exist_ok=True)

    def get_base_path(self) -> pathlib.Path:
        """Vrací základní adresář.

        Returns:
            Cesta k základnímu adresáři.

        Raises:
            ValueError: Pokud základní cesta nebyla nastavena.
        """
        if self._base_dir is None:
            raise ValueError("Base path has not been set.")
        return self._base_dir

    def base_data_path(self) -> pathlib.Path:
        """Vrací cestu ke složce s daty.

        Returns:
            Cesta ke složce 'data' v základním adresáři.

        Raises:
            ValueError: Pokud základní cesta nebyla nastavena.
        """
        if self._base_dir is None:
            raise ValueError("Base path has not been set.")
        return self._base_dir / "data"

    def data_path(self, filename: str) -> pathlib.Path:
        """Vrací cestu k souboru s daným názvem.

        Parametry:
            filename: Název souboru v adresáři data.

        Returns:
            Cesta k souboru.

        Raises:
            ValueError: Pokud soubor neexistuje.
        """
        file = self.base_data_path() / filename
        if not file.exists():
            raise ValueError(f"File {file.as_posix()} does not exist.")
        return file

    def base_save_data_path(self) -> pathlib.Path:
        """Vrací cestu ke složce pro uložení dat.

        Returns:
            Cesta ke složce 'data/saved', kterou vytvoří, pokud neexistuje.
        """
        path = self.base_data_path() / "saved"
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        return path

    def save_data_path(self, filename: str, delete_if_exist: bool = False) -> pathlib.Path:
        """Vrací cestu k souboru pro uložení dat.

        Parametry:
            filename: Název souboru pro uložení.
            delete_if_exist: Pokud True, smaže existující soubor (výchozí: False).

        Returns:
            Cesta k souboru pro uložení.

        Warns:
            UserWarning: Pokud soubor již existuje.
        """
        path = self.base_save_data_path() / filename
        if path.exists():
            warnings.warn(f"File {path.as_posix()} exists.")
            if delete_if_exist:
                warnings.warn("File was deleted!")
                path.unlink()
        return path
