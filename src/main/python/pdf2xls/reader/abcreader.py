from abc import ABC
from abc import abstractmethod
from typing import List

from ..model import Info


class ABCReader(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def read_infos(self) -> List[Info]:
        'eagerly read self.name'
