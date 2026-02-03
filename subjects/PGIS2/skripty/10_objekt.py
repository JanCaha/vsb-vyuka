class Zamestnanec:
    """Třída reprezentující zaměstnance. Zaměstnanec má jméno a hodinový plat."""

    def __init__(self, jmeno: str, hodinovy_plat: float):
        self.jmeno = jmeno
        self._hodinovy_plat = hodinovy_plat
        self.uvazek = 1.0

    def plat(self) -> float:
        """Funkce vrátí hodinový plat zaměstnance."""
        return self._hodinovy_plat

    def nastav_plat(self, hodinovy_plat: float) -> None:
        """Funkce nastaví hodinový plat zaměstnance."""
        self._hodinovy_plat = hodinovy_plat

    def zvys_plat(self, navyseni_o: float) -> None:
        """Funkce zvýší hodinový plat zaměstnance o zadanou hodnotu."""
        self._hodinovy_plat += navyseni_o

    def mesicni_plat(self, odpracovanych_hodin: float) -> float:
        """Funkce vrátí měsíční plat zaměstnance za zadaný počet odpracovaných hodin."""
        return self._hodinovy_plat * odpracovanych_hodin

    # statická metoda, jedná se o ukázku, ale zde by mohla být i normální metoda
    @staticmethod
    def delka_pracovniho_dne(uvazek: float = 1.0) -> float:
        """Statická metoda vrací délku pracovního dne zaměstnance dle výše úvazku."""
        return 8 * uvazek

    @property
    def pracovnich_hodin_denne(self) -> float:
        """Vrací délku pracovního dne zaměstnance dle výše úvazku."""
        return self.delka_pracovniho_dne(self.uvazek)

    @property
    def denni_plat(self) -> float:
        """Property vrací denní plat zaměstnance za 8 hodin práce."""
        return self._hodinovy_plat * self.pracovnich_hodin_denne

    def __repr__(self) -> str:
        return f"{self.jmeno} s denním platem {self.denni_plat}."

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Zamestnanec):
            return self.jmeno == value.jmeno
        else:
            raise NotImplementedError


if __name__ == "__main__":
    # tvorba instance třídy zamestnanec
    zam = Zamestnanec("Testovaci Zamestnanec", 250)
    # nastavení odpracovaných hodin
    odpracovane_hodiny = 160
    print(f"Denní plat: {zam.denni_plat}")
    print(f"Plat: {zam.mesicni_plat(odpracovane_hodiny)}")
    # navýšení platu
    zam.zvys_plat(50)
    print(f"Plat po zvýšení: {zam.mesicni_plat(odpracovane_hodiny)}")

    # změna úvazku
    zam.uvazek = 0.5
    print(f"Denní plat: {zam.denni_plat} při úvazku {zam.uvazek}")

    # tisk zaměstnance
    print(zam)

    # porovnání dvou zaměstnanců
    print(zam == Zamestnanec("Zamestnanec AB", 0))
