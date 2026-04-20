# NOTE: Ukázka použití kontextového manageru pro práci s vrstvou
# v utils.py třída LayerContextManager !!!
from osgeo import gdal, osr
from utils import LayerContextManager, data_path

gdal.UseExceptions()

if __name__ == "__main__":
    file_path = data_path("ne_10m_admin_0_countries.shp")

    with LayerContextManager(file_path) as layer:
        print(f"Název vrstvy: {layer.GetName()}")
        print(f"Počet prvků: {layer.GetFeatureCount()}")

        # objekt souřadnicového systému
        srs: osr.SpatialReference = layer.GetSpatialRef()

        # všimněte si použití `None` pro získání info o SRS
        print(f"Souřadnicový systém: {srs.GetAuthorityName(None)}:{srs.GetAuthorityCode(None)}")
