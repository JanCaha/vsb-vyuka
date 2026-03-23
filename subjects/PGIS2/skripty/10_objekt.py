# NOTE: Ukázka objektů, vlastností, statických metod a dědičnosti podle navazující prezentace
from typing import List, Tuple


class Polygon:
    """Třída reprezentující polygon definovaný seznamem vrcholů."""

    def __init__(self, vertices: List[Tuple[float, float]]):
        self.vertices = vertices

    def add_vertex(self, vertex: Tuple[float, float]) -> None:
        """Přidá vrchol do polygonu."""
        self.vertices.append(vertex)

    @staticmethod
    def is_closed(vertices: List[Tuple[float, float]]) -> bool:
        """Vrací True, pokud je polygon uzavřený (první a poslední vrchol jsou stejné)."""
        return vertices[0] == vertices[-1]

    def close(self) -> None:
        """Pokud polygon není uzavřený, uzavře jej přidáním prvního vrcholu na konec."""
        if self.is_closed(self.vertices):
            return
        self.vertices.append(self.vertices[0])

    def perimeter(self) -> float:
        """Spočítá obvod polygonu."""
        if len(self.vertices) < 2:
            return 0.0

        perimeter_value = 0.0
        for index in range(len(self.vertices) - 1):
            x1, y1 = self.vertices[index]
            x2, y2 = self.vertices[index + 1]
            perimeter_value += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        return perimeter_value

    @property
    def vertex_count(self) -> int:
        """Vrací počet vrcholů polygonu."""
        return len(self.vertices)

    @property
    def bounds(self) -> Tuple[float, float, float, float]:
        """Vrací obálku polygonu ve formátu (min_x, min_y, max_x, max_y)."""
        x_values = [x for x, _ in self.vertices]
        y_values = [y for _, y in self.vertices]
        return min(x_values), min(y_values), max(x_values), max(y_values)

    def __repr__(self) -> str:
        return f"Polygon s {self.vertex_count} vrcholy. Hranice: {self.bounds}"


class Rectangle(Polygon):
    """Potomek třídy Polygon reprezentující obdélník."""

    def __init__(self, x: float, y: float, width: float, height: float):
        vertices: List[Tuple[float, float]] = [
            (x, y),
            (x + width, y),
            (x + width, y + height),
            (x, y + height),
            (x, y),
        ]
        super().__init__(vertices)
        self.width = width
        self.height = height

    @classmethod
    def from_opposite_corners(
        cls,
        point_a: Tuple[float, float],
        point_b: Tuple[float, float],
    ) -> "Rectangle":
        """Vytvoří obdélník ze dvou protilehlých bodů zadaných jako dvojice (x, y)."""
        x1, y1 = point_a
        x2, y2 = point_b

        min_x = min(x1, x2)
        min_y = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)

        return cls(min_x, min_y, width, height)

    def area(self) -> float:
        """Vrací obsah obdélníku."""
        return self.width * self.height

    # přepsaná metoda pro výpočet obvodu obdélníku
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

    # přepsaná metoda pro reprezentaci obdélníku
    def __repr__(self) -> str:
        return f"Obdélník {self.width}x{self.height}, hranice: {self.bounds}"


if __name__ == "__main__":
    # ukázka objektu Polygon
    polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    print(f"Polygon je uzavřený: {Polygon.is_closed(polygon.vertices)}")
    polygon.close()
    print(f"Počet vrcholů polygonu: {polygon.vertex_count}")
    print(f"Obvod polygonu: {polygon.perimeter():.2f}")
    print(f"Obálka polygonu: {polygon.bounds}")
    print(polygon)
    print("-" * 20)

    # ukázka dědičnosti přes třídu Rectangle
    rectangle = Rectangle(0, 0, 5, 3)
    print(rectangle)
    print(f"Obsah obdélníku: {rectangle.area()}")
    print(f"Obvod obdélníku: {rectangle.perimeter()}")
    print(f"Je polygon: {isinstance(rectangle, Polygon)}")
    print(f"Je obdélník: {isinstance(rectangle, Rectangle)}")

    # ukázka tvorby obdélníku z protilehlých bodů
    rectangle_from_points = Rectangle.from_opposite_corners((2, 5), (-1, 1))
    print(rectangle_from_points)
    print(f"Obsah obdélníku z bodů: {rectangle_from_points.area()}")
