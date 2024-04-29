import polars as pl
from utils import data_path, save_data_path

if __name__ == "__main__":
    df = pl.read_csv(data_path("diamonds.csv"))

    print(df)
    print(df.describe())

    print(df.shape)
    print(df.columns)
    print(df.dtypes)
    print(df.schema)

    df_diamonds_e = df.filter(pl.col("color") == "E")

    print(df_diamonds_e)

    df_diamonds_e = df_diamonds_e.with_columns((pl.col("x") * pl.col("y") * pl.col("z")).cast(pl.Int64).alias("volume"))

    price = df_diamonds_e.get_column("price").to_list()

    df_diamonds_grouped = df.groupby(["cut", "color"]).agg(
        pl.col("price").median().alias("median_price"), pl.col("price").mean().alias("mean_price")
    )

    print(df_diamonds_grouped)

    df_diamonds_grouped.write_csv(save_data_path("diamonds_grouped.csv"))
