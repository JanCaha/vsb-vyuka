from pathlib import Path

import arcpy
import muj_balik
import muj_balik.location
import muj_balik.utils


def test_umisteni_baliku():
    folder = muj_balik.location.umisteni_baliku()
    assert Path(folder).exists()


def test_is_projected():
    crs = arcpy.SpatialReference(4326)
    assert muj_balik.utils.is_projected(crs) is False
    assert not muj_balik.utils.is_projected(crs)

    crs = arcpy.SpatialReference(5514)
    assert muj_balik.utils.is_projected(crs)
