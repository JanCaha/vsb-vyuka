import argparse
import pathlib
import re

import psycopg


def _cursor_has_results(cursor: psycopg.Cursor) -> bool:
    """Check if cursor has results."""
    return cursor.rowcount > 0 and cursor.statusmessage is not None and "SELECT" in cursor.statusmessage


def parse_args(arg_list: list[str] | None):
    """Parse arguments."""

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

    args = parser.parse_args(arg_list)
    return args


def eval_file(file: pathlib.Path, conn: psycopg.Connection):
    """Evaluate SQL file."""
    print("-" * 80)
    print(f"Running {file}...")

    with open(file, "r", encoding="UTF-8") as f:
        sql_file = f.read()

    sql_file = re.sub("--[\\w\\s();]+\\n", "", sql_file)
    sql_file = re.sub("\\/\\*[\\w\\s();\\W]+\\*\\/", "", sql_file)
    sql_file = re.sub("\\n", "", sql_file)

    sqls = sql_file.split(";")
    sqls = [sql.strip() for sql in sqls if sql]

    for sql in sqls:
        print(f"SQL: `{sql}`")
        print("+" * 10)
        with conn.cursor() as cur:
            cur.execute(sql)
            if _cursor_has_results(cur):
                print(cur.fetchall())
            else:
                print(cur.statusmessage)
        print("*" * 25)

    print("-" * 80)


def eval_files(sql_folder: pathlib.Path, conn: psycopg.Connection):
    """Eval SQL files in folder."""
    files = [file for file in sql_folder.glob("*.sql")]
    files.sort(key=lambda file: file.as_posix())

    for file in files:
        eval_file(file, conn)


def main(arg_list: list[str] | None = None):
    """Main function to be run."""
    args = parse_args(arg_list)

    eval_files(args.sql_folder, psycopg.connect(args.db_connection))


if __name__ == "__main__":
    main()
