import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import ListedColormap

url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/diamonds.csv"

df = pd.read_csv(url)

print(df)
print(df.dtypes)

# Výpočet objemu diamantu na základě proměnných x, y, z
df["volume"] = df["x"] * df["y"] * df["z"]

# Výpočet ceny za objem diamantu
df["price_per_volume"] = df["price"] / df["volume"]
df["price_per_volume"] = df["price_per_volume"].replace(
    [float("inf"), -float("inf")], float("nan")
)  # Nahrazení nekonečných hodnot NaN

# Výpis prvních několika řádků s novým sloupcem objemu
print(df[["x", "y", "z", "volume", "price_per_volume"]].head())

# Filtrování diamantů s cenou nad 2000
filtered_df = df[df["price"] > 2000]

# Zgrupování podle řezu a barvy a výpočet průměrné ceny ve skupině
grouped = filtered_df.groupby(["cut", "color"])["price"].mean().reset_index()

# Seřazení výsledku podle barvy
grouped = grouped.sort_values(by="color")

# Výpis výsledku
print(grouped)

# Vytvoření grafu závislosti karátů na ceně
plt.figure(figsize=(10, 6))
# Přidání barevné legendy podle barvy diamantu
# Definování kategorické palety barev

# Definování kategorické barevné škály
unique_colors = df["color"].unique()
color_map = ListedColormap(plt.cm.tab10.colors[: len(unique_colors)])

scatter = plt.scatter(
    df["carat"],
    df["price"],
    c=df["color"].astype("category").cat.codes,
    cmap=color_map,
    alpha=0.5,
    edgecolor="k",
)
# Vytvoření legendy bez poloprůhlednosti barev
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
