import argparse
import pathlib

import psycopg


def main():

    parser = argparse.ArgumentParser(
        prog="sql_runner.py",
        description="Run SQL scripts from folder and show outputs.",
        epilog="Author: Jan Caha",
    )

    parser.add_argument(
        "sql_folder",
        help="Folder with SQL scripts to run.",
        type=pathlib.Path,
    )

    parser.add_argument(
        "db_connection",
        help="Database connection string.",
    )

    args = parser.parse_args()

    sql_folder: pathlib.Path = args.sql_folder

    conn = psycopg.connect(args.db_connection)

    files = [file for file in sql_folder.glob("*.sql")]
    files.sort(key=lambda file: file.as_posix())

    for file in files:
        print("-" * 80)
        print(f"Running {file}...")

        with open(file, "r", encoding="UTF-8") as f:
            sql = f.read()

        with conn.cursor() as cur:
            cur.execute(sql)

        print("Done.")


if __name__ == "__main__":
    main()
