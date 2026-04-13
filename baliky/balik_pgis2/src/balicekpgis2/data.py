import pathlib
import zipfile

import requests
from balicekpgis2.paths import cache_file, extracted_folder

# adresář s datovými soubory balíčku
_DATA_DIR = pathlib.Path(__file__).parent / "data"

# Výchozí timeout pro stahování souborů (v sekundách)
_DOWNLOAD_TIMEOUT = 30


def _download_file(url: str, dest: pathlib.Path, timeout: int = _DOWNLOAD_TIMEOUT) -> None:
    """Stáhne soubor z URL a uloží ho na zadanou cestu.

    Parametry:
        url: Adresa pro stažení souboru.
        dest: Cílová cesta pro uložení.
        timeout: Timeout v sekundách (výchozí: 30).

    Raises:
        RuntimeError: Pokud se stažení nepovede.
    """

    try:
        response = requests.get(url, stream=True, timeout=timeout)
        response.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to download file from {url}: {e}") from e


def _extract_zip_to_dir(zip_path: pathlib.Path, extract_dir: pathlib.Path) -> None:
    """Rozbalí ZIP soubor do zadaného adresáře."""
    if extract_dir.exists():
        return

    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
    except zipfile.BadZipFile as e:
        raise


def _add_file_to_uri(url: str, file: str) -> str:
    """Přidá název souboru k URL, pokud není již přítomen."""
    if url.endswith(file):
        return url
    elif url.endswith("/"):
        return url + file
    else:
        return url + "/" + file


def _get_data(url: str, file: str, file_in_zip: str) -> pathlib.Path:
    """Stáhne soubor z URL a uloží ho do cache adresáře."""
    url = _add_file_to_uri(url, file)
    zip_path = cache_file(file)
    extract_dir = extracted_folder(pathlib.Path(file).stem)

    _download_file(url, zip_path)
    _extract_zip_to_dir(zip_path, extract_dir)

    result_file = extract_dir / file_in_zip
    if not result_file.exists():
        raise FileNotFoundError(f"Soubor '{file_in_zip}' nebyl nalezen v ZIP archivu.")

    return result_file


# Veřejné funkce, dostupné mimo tento modul


def data_countries() -> pathlib.Path:
    """Stáhne a rozbalí soubor s hranicemi zemí z Natural Earth."""
    return _get_data(
        "https://naciscdn.org/naturalearth/10m/cultural", "ne_10m_admin_0_countries.zip", "ne_10m_admin_0_countries.shp"
    )


def data_shaded_relief() -> pathlib.Path:
    """Stáhne a rozbalí soubor s reliéfním stínováním z Natural Earth."""
    return _get_data("https://naciscdn.org/naturalearth/50m/raster/", "NE1_50M_SR_W.zip", "NE1_50M_SR_W.tif")


def data_file_path(filename: str) -> pathlib.Path:
    """Vrátí cestu k datovému souboru v balíčku.

    Parametry:
        filename: Název souboru v datovém adresáři.

    Returns:
        Cesta k souboru.

    Raises:
        FileNotFoundError: Pokud soubor neexistuje.
    """
    path = _DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    return path


def read_text_file(filename: str) -> str:
    """Načte obsah textového souboru z datového adresáře balíčku.

    Parametry:
        filename: Název textového souboru.

    Returns:
        Obsah souboru v UTF-8 kódování.

    Raises:
        FileNotFoundError: Pokud soubor neexistuje.
    """
    path = data_file_path(filename)
    return path.read_text(encoding="utf-8")
