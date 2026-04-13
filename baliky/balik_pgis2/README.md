# Balíček `balicekpgis2`

Pomocný balíček pro předmět PGIS2 s užitečnými nástroji pro práci s GIS daty.

## Instalace

```bash
pip install -e .
```

## Funkce

### Context manageři
- `LayerContextManager` – Automatické otevírání a zavírání OGR vrstev
- `LayerFromDatasetContextManager` – Práce s vrstvami z existujícího gdal.Dataset
- `BandAsArrayContextManager` – Přístup k rastrovým pásmům

### Správa dat
- `data_countries()` – Stáhne hranice zemí z Natural Earth
- `data_shaded_relief()` – Stáhne reliéfní stínování z Natural Earth
- `data_file_path(filename)` – Přístup k lokálním datovým souborům
- `read_text_file(filename)` – Čtení textových souborů z balíčku

### Správa cest
- `PathManager` – Singleton pro správu základní cesty skriptu
- `cache_file(filename)` – Cesty do cache adresáře
- `extracted_folder(filename)` – Cesty do extrahovaných souborů

## Příklady

### Čtení vektorové vrstvy
```python
from balicekpgis2 import LayerContextManager
import pathlib

with LayerContextManager(pathlib.Path("data.shp")) as layer:
    for feature in layer:
        geom = feature.GetGeometryRef()
        print(geom.ExportToWkt())
```

### Stažení dat
```python
from balicekpgis2 import data_countries

countries_path = data_countries()
print(f"Soubor uložen v: {countries_path}")
```

### Správa cest
```python
from balicekpgis2 import PathManager

pm = PathManager()
pm.set_base_path(pathlib.Path("./my_project"))
data = pm.data_path("mydata.shp")
```

## Závislosti
- GDAL >= 3.10.0
- requests >= 2.32.3