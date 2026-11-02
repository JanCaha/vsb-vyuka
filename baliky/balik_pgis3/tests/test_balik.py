from pathlib import Path

import arcpy
from pgis3 import umisteni_baliku
from pgis3.utils import is_projected, normalize_name


def test_umisteni_baliku():
    folder = umisteni_baliku()
    assert Path(folder).exists()


def test_is_projected():
    crs = arcpy.SpatialReference(4326)
    assert is_projected(crs) is False
    assert not is_projected(crs)

    crs = arcpy.SpatialReference(5514)
    assert is_projected(crs)


def test_normalize_name_variants():
    assert normalize_name("Městské části 2024") == "mestske_casti_2024"
    assert normalize_name("Obec Č. 5") == "obec_c_5"
    assert normalize_name("  Praha-západ  ") == "praha_zapad"
    assert normalize_name("A/B\\C") == "a_b_c"
