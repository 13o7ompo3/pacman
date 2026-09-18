import numpy as np
import numpy.typing as npt


class Vec2:
    def __init__(self, *args) -> None:
        match len(args):
            case 0:
                x, y = 0.0, 0.0
            case 1:
                if isinstance(args[0], (float, int)):
                    x, y = (args[0],) * 2
                else:
                    x, y = args[0]
            case _:
                x, y = args

        self.array = np.array([float(x), float(y)])

    @classmethod
    def from_array(cls, array: npt.NDArray) -> "Vec2":
        new = cls()
        new.array = array
        return new

    @property
    def x(self) -> float:
        return float(self.array[0])

    @property
    def y(self) -> float:
        return float(self.array[1])

    @x.setter
    def x(self, value: float | float) -> None:
        self.array[0] = float(value)

    @y.setter
    def y(self, value: float | float) -> None:
        self.array[1] = float(value)

    def __add__(self, other: "Vec2 | tuple[float, float]") -> "Vec2":
        if isinstance(other, tuple):
            x, y = other
            return Vec2(self.x + x, self.y + y)
        return Vec2.from_array(self.array + other.array)

    def __sub__(self, other: "Vec2 | tuple[float, float]") -> "Vec2":
        if isinstance(other, tuple):
            x, y = other
            return Vec2(self.x - x, self.y - y)
        return Vec2.from_array(self.array - other.array)

    def __mul__(self, scalar: float) -> "Vec2":
        return Vec2.from_array(self.array * scalar)

    def __truediv__(self, scalar: float) -> "Vec2":
        return Vec2.from_array(self.array / scalar)

    def __str__(self) -> str:
        return f"Vec2({self.x}, {self.y})"

    __repr__ = __str__

    def __getitem__(self, i: int) -> float:
        return self.array[i]

    def __setitem__(self, i: int, value: float) -> None:
        self.array[i] = value

    def __len__(self) -> float:
        return 2

    def __hash__(self) -> int:
        return int(self.x * 31 + self.y)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Vec2) and self.x == other.x and self.y == other.y
        )

    def copy(self) -> "Vec2":
        return Vec2(self.x, self.y)

    def move_towards(self, other: "Vec2", distance: float) -> "Vec2":
        mag = np.linalg.norm(self.array - other.array)
        distance = min(distance, mag)
        ratio = distance / mag if mag else 0
        result = Vec2(
            self.x + (other.x - self.x) * ratio,
            self.y + (other.y - self.y) * ratio,
        )
        return result
