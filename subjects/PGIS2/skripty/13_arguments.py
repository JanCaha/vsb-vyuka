import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(prog="calculate", description="Skript pro výpočet hodnoty.")

    # Definice argumentů
    parser.add_argument("a", help="Hodnota a", type=float)  # povinný poziční argument
    parser.add_argument("b", help="Hodnota b", type=float)  # povinný poziční argument
    parser.add_argument(
        "-o", "--operator", help="Operátor s hodnotami", default="*", type=str, choices=["*", "/", "+", "-"]
    )  # volitelný argument s výchozí hodnotou "*"
    parser.add_argument(
        "-r", "--result", help="Výsledný soubor", type=Path, default=Path("vysledek.txt")
    )  # volitelný argument s výchozí hodnotou "vysledek.txt"
    parser.add_argument(
        "-v", "--verbose", help="Zobrazit podrobnosti", action="store_true"
    )  # volitelný argument pro zobrazení podrobností

    # Zpracování argumentů
    args = parser.parse_args()

    result = 0
    if args.operator == "*":
        result = float(args.a) * float(args.b)
    elif args.operator == "/":
        result = float(args.a) / float(args.b)
    elif args.operator == "+":
        result = float(args.a) + float(args.b)
    elif args.operator == "-":
        result = float(args.a) - float(args.b)

    if args.verbose:
        print(f"Podrobnosti: {args.a} {args.operator} {args.b} = {result}")

    # Uložení výsledku do souboru
    with open(args.result, "w", encoding="utf-8") as file:
        file.write(f"Výsledek: {result}\n")


if __name__ == "__main__":
    main()
