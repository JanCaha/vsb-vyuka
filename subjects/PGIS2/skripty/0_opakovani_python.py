with open("soubor.txt", "w", encoding="utf-8") as file:

    for i in range(10):
        file.write(f"{i}\n")
