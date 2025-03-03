# NOTE: v utils.py třída LayerContextManager !!!
import utils
from osgeo import osr

if __name__ == "__main__":
    data_path = utils.data_path("ne_10m_admin_0_countries.shp")

    with utils.LayerContextManager(data_path) as layer:
        print(f"Název vrstvy: {layer.GetName()}")
        print(f"Počet prvků: {layer.GetFeatureCount()}")

        # objekt souřadnicového systému
        srs: osr.SpatialReference = layer.GetSpatialRef()

        # všimněte si použití `None` pro získání info o SRS
        print(f"Souřadnicový systém: {srs.GetAuthorityName(None)}:{srs.GetAuthorityCode(None)}")
