from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import List

from ..model import Info


class ABCWriter(ABC):
    def __init__(self, name: Path):
        self.name = name

    @abstractmethod
    def write_infos(self, infos: List[Info]) -> None:
        'append an info to a file - returns mtime'
