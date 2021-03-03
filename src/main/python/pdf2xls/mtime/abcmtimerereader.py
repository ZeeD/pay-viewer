'ABC for the mtime readers'

from abc import ABC
from abc import abstractmethod
from datetime import datetime
from typing import BinaryIO
from typing import TextIO
from typing import Union

UnionIO = Union[BinaryIO, TextIO]


class ABCMtimeReader(ABC):
    'define an mtime reader'

    def __init__(self, info_file: UnionIO):
        self.info_file = info_file

    @abstractmethod
    def mtime(self) -> datetime:
        'retrieve the mtime of the info_file'
