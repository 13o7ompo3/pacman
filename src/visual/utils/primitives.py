from typing import Iterator, Tuple, Union, Any

import numpy as np
import numpy.typing as npt


class Vec2:
    def __init__(
        self, *args: Union[float, int, Tuple[float, float], "Vec2"]
    ) -> None:
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

        self.array: npt.NDArray[np.floating[Any]] = np.array(
            [float(x), float(y)]
        )

    @classmethod
    def from_array(cls, array: npt.NDArray[np.floating[Any]]) -> "Vec2":
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
    def x(self, value: float) -> None:
        self.array[0] = value

    @y.setter
    def y(self, value: float) -> None:
        self.array[1] = value

    def __add__(self, other: Union["Vec2", Tuple[float, float]]) -> "Vec2":
        if isinstance(other, tuple):
            x, y = other
            return Vec2(self.x + x, self.y + y)
        return Vec2.from_array(self.array + other.array)

    def __sub__(self, other: Union["Vec2", Tuple[float, float]]) -> "Vec2":
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
        return float(self.array[i])

    def __setitem__(self, i: int, value: float) -> None:
        self.array[i] = value

    def __delitem__(self, i: int) -> None:
        self.array[i] = 0

    def __len__(self) -> int:
        return 2

    def __hash__(self) -> int:
        return int(self.x * 31 + self.y)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Vec2) and self.x == other.x and self.y == other.y
        )

    def __iter__(self) -> Iterator[float]:
        yield self.x
        yield self.y

    def copy(self) -> "Vec2":
        return Vec2(self.x, self.y)

    def distance_to(self, other: "Vec2") -> float:
        return np.linalg.norm(self.array - other.array)

    def move_towards(self, other: "Vec2", distance: float) -> "Vec2":
        mag = float(np.linalg.norm(self.array - other.array))
        distance = min(distance, mag)
        ratio = distance / mag if mag else 0.0
        result = Vec2(
            self.x + (other.x - self.x) * ratio,
            self.y + (other.y - self.y) * ratio,
        )
        return result

    def as_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)


class Rect:
    def __init__(
        self,
        pos: Union[Vec2, Tuple[float, float]],
        size: Union[Vec2, Tuple[float, float]],
    ) -> None:
        if isinstance(pos, tuple):
            pos = Vec2(pos)
        self.pos: Vec2 = pos.copy()
        if isinstance(size, tuple):
            size = Vec2(size)
        self.size: Vec2 = size.copy()

    @property
    def x(self) -> float:
        return self.pos.x

    @x.setter
    def x(self, value: float) -> None:
        self.pos[0] = value

    @property
    def y(self) -> float:
        return self.pos.y

    @y.setter
    def y(self, value: float) -> None:
        self.pos[1] = value

    @property
    def width(self) -> float:
        return self.size.x

    @width.setter
    def width(self, value: float) -> None:
        self.size[0] = value

    @property
    def height(self) -> float:
        return self.size.y

    @height.setter
    def height(self, value: float) -> None:
        self.size[1] = value

    @property
    def topleft(self) -> Vec2:
        return self.pos

    @topleft.setter
    def topleft(self, value: Union[Vec2, Tuple[float, float]]) -> None:
        if isinstance(value, tuple):
            value = Vec2(value)
        self.pos = value

    @property
    def center(self) -> Vec2:
        return self.pos + self.size / 2

    def collidepoint(self, x: float, y: float) -> bool:
        return (
            self.pos.x <= x < self.pos.x + self.size.x
            and self.pos.y <= y < self.pos.y + self.size.y
        )

    def inflate(self, x: float, y: float) -> "Rect":
        return Rect(self.pos - (x / 2, y / 2), self.size + (x, y))
