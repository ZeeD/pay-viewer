from abc import ABC
from abc import abstractmethod
from typing import List

from ..model import Info


class ABCWriter(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def write_infos(self, infos: List[Info]) -> None:
        'append an info to a file - returns mtime'
