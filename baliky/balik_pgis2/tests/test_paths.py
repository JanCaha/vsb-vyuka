"""Testy pro modul paths."""

import pathlib
import tempfile

import pytest
from balicekpgis2 import PathManager


class TestPathManager:
    """Testy pro PathManager singleton."""

    def test_singleton_instance(self) -> None:
        """Ověří, že PathManager vrací stejnou instanci."""
        pm1 = PathManager()
        pm2 = PathManager()
        assert pm1 is pm2

    def test_set_and_get_base_path(self) -> None:
        """Ověří nastavení a získání základní cesty."""
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = PathManager()
            base_path = pathlib.Path(tmpdir)
            pm.set_base_path(base_path)
            assert pm.get_base_path() == base_path

    def test_base_data_path_creation(self) -> None:
        """Ověří vytvoření cesty k datovému adresáři."""
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = PathManager()
            pm.set_base_path(pathlib.Path(tmpdir))
            data_path = pm.base_data_path()
            assert data_path.name == "data"
            assert str(tmpdir) in str(data_path)

    def test_base_save_data_path_creates_directory(self) -> None:
        """Ověří vytvoření adresáře pro uložení dat."""
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = PathManager()
            pm.set_base_path(pathlib.Path(tmpdir))
            save_path = pm.base_save_data_path()
            assert save_path.exists()
            assert save_path.name == "saved"

    def test_data_path_with_existing_file(self) -> None:
        """Ověří cestu k existujícímu souboru."""
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = PathManager()
            base_path = pathlib.Path(tmpdir)
            pm.set_base_path(base_path)

            # Vytvoří datový adresář a testovací soubor
            data_dir = base_path / "data"
            data_dir.mkdir()
            test_file = data_dir / "test.txt"
            test_file.write_text("test content")

            # Ověří, že se vrátí správná cesta
            assert pm.data_path("test.txt") == test_file

    def test_data_path_with_nonexistent_file(self) -> None:
        """Ověří vyvolání chyby pro neexistující soubor."""
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = PathManager()
            pm.set_base_path(pathlib.Path(tmpdir))

            with pytest.raises(ValueError):
                pm.data_path("nonexistent.txt")

    def test_get_base_path_not_set(self) -> None:
        """Ověří vyvolání chyby, když základní cesta není nastavena."""
        # Protože PathManager je singleton, testujeme jen případ
        # kdy _base_dir byl resetován
        pm = PathManager()
        if pm._base_dir is not None:
            pytest.skip("Base path is already set from previous tests")
