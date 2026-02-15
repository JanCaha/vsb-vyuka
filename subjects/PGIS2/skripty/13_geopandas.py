# NOTE: Ukázka práce s knihovnou geopandas - načtení geodat, prostorové operace,
# vizualizace a export do GeoPackage
import geopandas as gpd
import matplotlib.pyplot as plt
import utils

if __name__ == "__main__":
    # načtení vektorových dat do GeoDataFrame
    file = utils.data_path("ne_10m_admin_0_countries.shp")
    gdf: gpd.GeoDataFrame = gpd.read_file(file)

    # základní informace o datech
    print(f"Počet prvků (řádků): {len(gdf)}")
    print(f"Sloupce: {list(gdf.columns)}")
    print(f"Souřadnicový systém: {gdf.crs}")
    print(f"Rozsah dat: {gdf.total_bounds}")
    print("-" * 50)

    # výběr sloupců a prvních řádků
    print(gdf[["NAME", "CONTINENT", "POP_EST", "GDP_MD"]].head(10))
    print("-" * 50)

    # filtrování - státy v Evropě
    europe: gpd.GeoDataFrame = gdf[gdf["CONTINENT"] == "Europe"].copy()
    print(f"Počet evropských států: {len(europe)}")

    # transformace souřadnicového systému do EPSG:3035 (ETRS89-extended / LAEA Europe)
    europe_projected: gpd.GeoDataFrame = europe.to_crs(epsg=3035)

    # výpočet plochy v km²
    europe_projected["area_km2"] = europe_projected.geometry.area / 1e6
    print(europe_projected[["NAME", "area_km2"]].sort_values("area_km2", ascending=False).head(10))
    print("-" * 50)

    # prostorová operace - buffer 50 km kolem geometrií
    europe_buffered: gpd.GeoDataFrame = europe_projected.copy()
    europe_buffered["geometry"] = europe_projected.geometry.buffer(50_000)

    # dissolve - sloučení všech geometrií podle kontinentu
    europe_dissolved: gpd.GeoDataFrame = europe_projected.dissolve(by="CONTINENT")
    print(f"Počet prvků po dissolve: {len(europe_dissolved)}")
    print("-" * 50)

    # spatial join - identifikace, které státy se protínají s vybraným státem
    czechia = europe_projected[europe_projected["NAME"] == "Czechia"]
    neighbors: gpd.GeoDataFrame = gpd.sjoin(
        europe_projected,
        czechia[["geometry"]],
        how="inner",
        predicate="intersects",
    )
    print(f"Státy sousedící s Českem (včetně): {list(neighbors['NAME'])}")
    print("-" * 50)

    # vizualizace - jednoduchá mapa Evropy s barvou podle populace
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    europe_projected.plot(
        column="POP_EST",
        cmap="YlOrRd",
        legend=True,
        legend_kwds={"label": "Population", "shrink": 0.6},
        edgecolor="black",
        linewidth=0.5,
        ax=ax,
    )
    ax.set_title("European Countries by Population", fontsize=14)
    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig("europe_population.png", dpi=300, bbox_inches="tight")

    # export výsledku do GeoPackage
    result_file = utils.save_data_path("europe_countries.gpkg", delete_if_exist=True)
    europe_projected.to_file(result_file, driver="GPKG", layer="countries")
    print(f"Data uložena do: {result_file.as_posix()}")
