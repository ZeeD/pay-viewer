from abc import ABC
from abc import abstractmethod
from pathlib import Path

from payviewer.model import Info


class ABCReader(ABC):
    def __init__(self, name: Path) -> None:
        self.name = name

    @abstractmethod
    def read_infos(self) -> list[Info]:
        ...
