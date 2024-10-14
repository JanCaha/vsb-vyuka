import random
from abc import ABC, abstractmethod


class RandomValueGenerator(ABC):

    @abstractmethod
    def random_value(self) -> float:
        """Vygeneruj náhodnou hodnotu"""

    def name(self) -> str:
        return "Random Generator"


class RandomIntGenerator(RandomValueGenerator):

    def __init__(self, min: int, max: int) -> None:
        super().__init__()
        self.min = min
        self.max = max

    def random_value(self) -> float:
        return float(random.randint(self.min, self.max))


class RandomFloatGenerator(RandomValueGenerator):

    def __init__(self, min: float, max: float, decimal_places: int = 6) -> None:
        super().__init__()
        self.min = min
        self.max = max
        self.decimal_places = decimal_places

    def _random_value(self) -> float:
        return random.random()

    def random_value(self) -> float:
        value = round(self.random_scaled_moved(), self.decimal_places)
        return value

    def width(self) -> float:
        return self.max - self.min

    def random_scaled_moved(self) -> float:
        return self._random_value() * self.width() + self.min

    def name(self) -> str:
        return "Random Float Generator"


class RandomSimpleGenerator(RandomValueGenerator):

    def random_value(self) -> float:
        return 42


def get_some_value(rnd: RandomValueGenerator) -> float:
    return rnd.random_value()


def print_message(rnd: RandomValueGenerator):
    print(f"{rnd.name()} - {get_some_value(rnd)}")


if __name__ == "__main__":
    # samotná třída interface nejde vytvořit - není kompletní
    # a = RandomValueGenerator()

    # třídy implementující interface vytvořit lze
    b = RandomIntGenerator(3, 5)
    print_message(b)

    c = RandomFloatGenerator(10, 25)
    print_message(c)

    d = RandomSimpleGenerator()
    print_message(d)
