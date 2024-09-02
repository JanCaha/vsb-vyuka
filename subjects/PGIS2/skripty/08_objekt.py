import typing


class Zamestnanec:
    """Třída reprezentující zaměstnance. Zaměstnanec má jméno a hodinový plat."""

    def __init__(self, jmeno: str, hodinovy_plat: float):
        self.jmeno = jmeno
        self._hodinovy_plat = hodinovy_plat
        self._srazka_z_platu: typing.Optional[float] = None

    def nastav_srazku_z_platu(self, srazka: typing.Optional[float] = None) -> None:
        """Funkce nastaví sražku z platu zaměstnance."""
        self._srazka_z_platu = srazka

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
        if self._srazka_z_platu:
            return self._hodinovy_plat * odpracovanych_hodin - self._srazka_z_platu
        else:
            return self._hodinovy_plat * odpracovanych_hodin

    @property
    def denni_plat(self) -> float:
        """Property vrací denní plat zaměstnance za 8 hodin práce."""
        return self._hodinovy_plat * 8

    def __repr__(self) -> str:
        return f"{self.jmeno} s denním platem {self._hodinovy_plat}."

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Zamestnanec):
            return self.jmeno == value.jmeno
        else:
            raise NotImplementedError


if __name__ == "__main__":
    odpracovane_hodiny = 160
    zam = Zamestnanec("Testovaci Zamestnanec", 250)
    print(f"Plat: {zam.mesicni_plat(odpracovane_hodiny)}")
    zam.zvys_plat(50)
    print(f"Plat po zvýšení: {zam.mesicni_plat(odpracovane_hodiny)}")
