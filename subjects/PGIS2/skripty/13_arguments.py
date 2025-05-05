import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(prog="calculate", description="Skript pro výpočet hodnoty.")

    # Definice argumentů
    parser.add_argument("a", help="Hodnota a", type=float)
    parser.add_argument("b", help="Hodnota b", type=float)
    parser.add_argument(
        "-o", "--operator", help="Operátor s hodnotami", default="*", type=str, choices=["*", "/", "+", "-"]
    )
    parser.add_argument("-r", "--result", help="Výsledný soubor", type=Path, default=Path("vysledek.txt"))

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

    # Uložení výsledku do souboru
    with open(args.result, "w", encoding="utf-8") as file:
        file.write(f"Výsledek: {result}\n")


if __name__ == "__main__":
    main()
