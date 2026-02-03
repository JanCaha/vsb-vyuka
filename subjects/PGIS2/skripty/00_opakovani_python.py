import random
from pathlib import Path

# cyklus který vypisuje sudá čísla, lichá se přeskočí
for i in range(10):
    if i % 2 == 0:
        continue
    print(f"Opakování číslo {i}")

print(f"Poslední hodnota: {i}")
print("*" * 50)  # oddělovač výstupu

# cyklus který vypisuje čísla, pokud je větší než 13, cyklus se ukončí
for i in range(15):
    if i > 13:
        break
    print(f"Opakování číslo {i}")

print(f"Poslední hodnota: {i}")
print("*" * 50)

# cyklus pro soubor hodnot, s použitím enumerate
values = [10, 9, 8, 7, 6, 5, 4]
for i, value in enumerate(values):
    print(f"Na pozici {i} je hodnota {value}")

print("*" * 50)

# cyklus bez známého počtu opakování
limit = 100
hodnota = 0

while hodnota < limit:
    hodnota = hodnota + random.randint(1, 10)
    print(f"Hodnota: {hodnota}")

print(f"Výsledná hodnota: {hodnota}")
print("*" * 50)

# zápis do souboru bez kontextového manažeru
file = open("soubor.txt", "w", encoding="utf-8")
file.write("Text")
file.close()  # na toto se zapomíná


# zápis do souboru s kontextovým manažerem
with open("soubor.txt", "w", encoding="utf-8") as file:
    file.write("Text")

# práce s objektem
cesta_k_souboru = Path(__file__)
print(f"Cesta k souboru: {cesta_k_souboru.as_posix()}")

nova_cesta_k_souboru = cesta_k_souboru.with_suffix(".txt")
print(f"Nová cesta k souboru: {nova_cesta_k_souboru.as_posix()}")

cesta_k_souboru_vedlejsi_slozka = cesta_k_souboru.parent / "jina_slozka" / "soubor.txt"
print(f"Cesta k souboru ve vedlejší složce: {cesta_k_souboru_vedlejsi_slozka.as_posix()}")
print(f"Soubor existuje: {cesta_k_souboru_vedlejsi_slozka.exists()}")
