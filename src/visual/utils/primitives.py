from typing import Union, Iterator

import numpy as np


class Vec2:
    """A 2D vector with basic arithmetic and sequence behavior.

    Attributes:
        x (float): The horizontal component.
        y (float): The vertical component.

    """

    def __init__(
        self, *args: Union[float, tuple[float, float], "Vec2"]
    ) -> None:
        """Create a vector from scalars, a pair, or another vector.

        Args:
            *args: No args, one scalar, one pair, or two scalars.

        Returns:
            None: This method initializes the vector in place.

        """
        self.x: float = 0.0
        self.y: float = 0.0

        match len(args):
            case 0:
                self.x, self.y = 0.0, 0.0
            case 1:
                if isinstance(args[0], (float, int)):
                    self.x, self.y = (args[0],) * 2
                else:
                    self.x, self.y = args[0]
            case 2:
                if isinstance(args[0], (int, float)) and isinstance(
                    args[1], (int, float)
                ):
                    self.x, self.y = args[0], args[1]

    def __add__(self, other: Union["Vec2", tuple[float, float]]) -> "Vec2":
        """Return the vector sum.

        Args:
            other: The vector or pair to add.

        Returns:
            Vec2: The resulting vector.

        """
        x, y = other
        return Vec2(self.x + x, self.y + y)

    def __sub__(self, other: Union["Vec2", tuple[float, float]]) -> "Vec2":
        """Return the vector difference.

        Args:
            other: The vector or pair to subtract.

        Returns:
            Vec2: The resulting vector.

        """
        x, y = other
        return Vec2(self.x - x, self.y - y)

    def __mul__(self, scalar: float) -> "Vec2":
        """Return this vector scaled by a number.

        Args:
            scalar: The scale factor.

        Returns:
            Vec2: The scaled vector.

        """
        return Vec2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> "Vec2":
        """Return this vector divided by a number.

        Args:
            scalar: The divisor.

        Returns:
            Vec2: The divided vector.

        """
        return Vec2(self.x / scalar, self.y / scalar)

    def __str__(self) -> str:
        """Return a readable string form.

        Returns:
            str: The string representation.

        """
        return f"Vec2({self.x}, {self.y})"

    __repr__ = __str__

    def __getitem__(self, i: int) -> float:
        """Return the requested component by index.

        Args:
            i: The component index.

        Returns:
            float: The requested component.

        """
        return (self.x, self.y)[i]

    def __setitem__(self, i: int, value: float) -> None:
        """Set the requested component by index.

        Args:
            i: The component index.
            value: The new component value.

        Returns:
            None: This method updates the vector in place.

        """
        if i == 0:
            self.x = value
        elif i == 1:
            self.y = value

    def __delitem__(self, i: int) -> None:
        """Reset the requested component to zero.

        Args:
            i: The component index.

        Returns:
            None: This method updates the vector in place.

        """
        if i == 0:
            self.x = 0
        elif i == 1:
            self.y = 0

    def __len__(self) -> int:
        """Return the number of vector components.

        Returns:
            int: The number of components.

        """
        return 2

    def __hash__(self) -> int:
        """Return a hash value for use in hash-based containers.

        Returns:
            int: The hash value.

        """
        return int(self.x * 31 + self.y)

    def __eq__(self, other: object) -> bool:
        """Return whether two vectors have the same components.

        Args:
            other: The object to compare.

        Returns:
            bool: True if both vectors are equal.

        """
        return (
            isinstance(other, Vec2) and self.x == other.x and self.y == other.y
        )

    def __iter__(self) -> Iterator[float]:
        """Yield the vector components in order.

        Returns:
            Iterator[float]: An iterator over the components.

        """
        yield self.x
        yield self.y

    def copy(self) -> "Vec2":
        """Return a copy of this vector.

        Returns:
            Vec2: A copy of the vector.

        """
        return Vec2(self.x, self.y)

    def distance_to(self, other: "Vec2") -> float:
        """Return the Euclidean distance to another vector.

        Args:
            other: The vector to measure from.

        Returns:
            float: The distance between both vectors.

        """
        return float(np.linalg.norm(np.array(self) - np.array(other)))

    def move_towards(self, other: "Vec2", distance: float) -> "Vec2":
        """Return a point moved toward another vector by a distance.

        Args:
            other: The target vector.
            distance: The maximum movement distance.

        Returns:
            Vec2: The moved vector.

        """
        mag = float(np.linalg.norm(np.array(self) - np.array(other)))
        distance = min(distance, mag)
        ratio = distance / mag if mag else 0.0
        result = Vec2(
            self.x + (other.x - self.x) * ratio,
            self.y + (other.y - self.y) * ratio,
        )
        return result

    def as_tuple(self) -> tuple[float, float]:
        """Return the vector as a plain tuple.

        Returns:
            tuple[float, float]: The vector components.

        """
        return (self.x, self.y)


class Rect:
    """A rectangle defined by a position and a size.

    Attributes:
        pos (Vec2): The top-left position.
        size (Vec2): The rectangle size.

    """

    def __init__(
        self,
        pos: Vec2 | tuple[float, float],
        size: Vec2 | tuple[float, float],
    ) -> None:
        """Create a rectangle from a position and a size.

        Args:
            pos: The top-left position.
            size: The rectangle size.

        Returns:
            None: This method initializes the rectangle in place.

        """
        if isinstance(pos, tuple):
            pos = Vec2(pos)
        self.pos: Vec2 = pos.copy()
        if isinstance(size, tuple):
            size = Vec2(size)
        self.size: Vec2 = size.copy()

    @property
    def x(self) -> float:
        """Return the x-coordinate of the rectangle.

        Returns:
            float: The x-coordinate.

        """
        return self.pos.x

    @x.setter
    def x(self, value: float) -> None:
        """Set the x-coordinate of the rectangle.

        Args:
            value: The new x-coordinate.

        Returns:
            None: This property setter updates the rectangle in place.

        """
        self.pos[0] = value

    @property
    def y(self) -> float:
        """Return the y-coordinate of the rectangle.

        Returns:
            float: The y-coordinate.

        """
        return self.pos.y

    @y.setter
    def y(self, value: float) -> None:
        """Set the y-coordinate of the rectangle.

        Args:
            value: The new y-coordinate.

        Returns:
            None: This property setter updates the rectangle in place.

        """
        self.pos[1] = value

    @property
    def width(self) -> float:
        """Return the rectangle width.

        Returns:
            float: The rectangle width.

        """
        return self.size.x

    @width.setter
    def width(self, value: float) -> None:
        """Set the rectangle width.

        Args:
            value: The new width.

        Returns:
            None: This property setter updates the rectangle in place.

        """
        self.size[0] = value

    @property
    def height(self) -> float:
        """Return the rectangle height.

        Returns:
            float: The rectangle height.

        """
        return self.size.y

    @height.setter
    def height(self, value: float) -> None:
        """Set the rectangle height.

        Args:
            value: The new height.

        Returns:
            None: This property setter updates the rectangle in place.

        """
        self.size[1] = value

    @property
    def topleft(self) -> Vec2:
        """Return the top-left position.

        Returns:
            Vec2: The rectangle position.

        """
        return self.pos

    @topleft.setter
    def topleft(self, value: Vec2 | tuple[float, float]) -> None:
        """Set the top-left position.

        Args:
            value: The new position.

        Returns:
            None: This property setter updates the rectangle in place.

        """
        if isinstance(value, tuple):
            value = Vec2(value)
        self.pos = value

    @property
    def center(self) -> Vec2:
        """Return the rectangle center.

        Returns:
            Vec2: The rectangle center point.

        """
        return self.pos + self.size / 2

    def collidepoint(self, x: float, y: float) -> bool:
        """Return whether a point lies inside the rectangle.

        Args:
            x: The x-coordinate of the point.
            y: The y-coordinate of the point.

        Returns:
            bool: True if the point is inside the rectangle.

        """
        return (
            self.pos.x <= x < self.pos.x + self.size.x
            and self.pos.y <= y < self.pos.y + self.size.y
        )

    def inflate(self, x: float, y: float) -> "Rect":
        """Return a new rectangle expanded by the given amounts.

        Args:
            x: The horizontal expansion amount.
            y: The vertical expansion amount.

        Returns:
            Rect: The expanded rectangle.

        """
        return Rect(self.pos - (x / 2, y / 2), self.size + (x, y))
