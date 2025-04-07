import typing

import polars as pl
from utils import data_path, save_data_path


def calculate_aggregates(column_name: str) -> typing.List[pl.Expr]:
    """Vytvoří výrazy pro výpočet mediánu a průměru pro zadaný sloupec."""
    expressions = []
    expressions.append(pl.col(column_name).median().alias(f"median_{column_name}"))
    expressions.append(pl.col(column_name).mean().alias(f"mean_{column_name}"))
    return expressions


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

    exprs = calculate_aggregates("price")
    exprs.extend(calculate_aggregates("x"))

    df_diamonds_grouped = df.group_by(["cut", "color"]).agg(exprs)

    print(df_diamonds_grouped)

    df_diamonds_grouped.write_csv(save_data_path("diamonds_grouped.csv"))


