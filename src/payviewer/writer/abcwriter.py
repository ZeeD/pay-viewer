from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from payviewer.model import Info


class ABCWriter(ABC):
    def __init__(self, name: 'Path') -> None:
        self.name = name

    @abstractmethod
    def write_infos(self, infos: list['Info']) -> None: ...
