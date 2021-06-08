from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import List

from ..model import Info


class ABCReader(ABC):
    def __init__(self, name: Path):
        self.name = name

    @abstractmethod
    def read_infos(self) -> List[Info]:
        'eagerly read self.name'
