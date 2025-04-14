import matplotlib.pyplot as plt
import polars as pl
from matplotlib.colors import ListedColormap

# Načtení dat z URL
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/diamonds.csv"
df = pl.read_csv(url)

# Výpis datového rámce a jeho typů
print(df)
print(df.dtypes)

# Výpočet objemu diamantu na základě proměnných x, y, z
df = df.with_columns((df["x"] * df["y"] * df["z"]).alias("volume"))

# Výpočet ceny za objem diamantu
df = df.with_columns((df["price"] / df["volume"]).alias("price_per_volume"))
df = df.with_columns(
    pl.when(pl.col("price_per_volume").is_infinite())
    .then(None)
    .otherwise(pl.col("price_per_volume"))
    .alias("price_per_volume")
)

# Výpis prvních několika řádků s novým sloupcem objemu
print(df.select(["x", "y", "z", "volume", "price_per_volume"]).head())

# Filtrování diamantů s cenou nad 2000
filtered_df = df.filter(df["price"] > 2000)

# Zgrupování podle řezu a barvy a výpočet průměrné ceny ve skupině
grouped = filtered_df.group_by(["cut", "color"]).agg(pl.col("price").mean().alias("mean_price")).sort("color")

# Výpis výsledku
print(grouped)

# Vytvoření grafu závislosti karátů na ceně
plt.figure(figsize=(10, 6))

# Definování kategorické palety barev
unique_colors = df.select("color").unique().to_series().to_list()
color_map = ListedColormap(plt.cm.tab10.colors[: len(unique_colors)])

plt.scatter(
    df["carat"].to_numpy(),
    df["price"].to_numpy(),
    c=df["color"].cast(pl.Categorical).to_physical(),
    cmap=color_map,
    alpha=0.5,
    edgecolor="k",
)

handles = [
    plt.Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        markerfacecolor=color_map(i),
        markersize=10,
        label=color,
    )
    for i, color in enumerate(unique_colors)
]
plt.legend(handles=handles, title="Color", fontsize=10, title_fontsize=12)

plt.title("Dependence of Price on Carat", fontsize=14)
plt.xlabel("Carat", fontsize=12)
plt.ylabel("Price", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.7)

# interaktivní zobrazení grafu
# plt.show()

# Uložení grafu do souboru
plt.savefig("price_vs_carat.png", dpi=300, bbox_inches="tight")
