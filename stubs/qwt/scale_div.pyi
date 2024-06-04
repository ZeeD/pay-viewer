from collections.abc import Sequence
from typing import overload

class QwtScaleDiv:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(
        self,
        lowerBound: float,  # noqa:N803
        upperBound: float,  # noqa:N803
    ) -> None: ...
    @overload
    def __init__(
        self,
        lowerBound: float,  # noqa:N803
        upperBound: float,  # noqa:N803
        ticks: list[Sequence[float]],
    ) -> None: ...
    @overload
    def __init__(
        self,
        lowerBound: float,  # noqa:N803
        upperBound: float,  # noqa:N803
        minorTicks: Sequence[float],  # noqa:N803
        mediumTicks: Sequence[float],  # noqa:N803
        majorTicks: Sequence[float],  # noqa:N803
    ) -> None: ...
    def setLowerBound(self, lowerBound: float) -> None: ...  # noqa:N802,N803
    def setUpperBound(self, upperBound: float) -> None: ...  # noqa:N802,N803
