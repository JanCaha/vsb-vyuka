import pathlib


def umisteni_baliku() -> str:
    """Funkce vrací umístění adresáře s touto funkcí."""
    file = pathlib.Path(__file__).parent.as_posix()
    return file
