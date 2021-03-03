'ABC for the readers'

from abc import abstractmethod
from datetime import datetime
from typing import Iterable

from ..model.info import Info
from ..mtime.abcmtimerereader import ABCMtimeReader
from ..mtime.abcmtimerereader import UnionIO


class ABCReader(ABCMtimeReader):
    'define a reader'

    def __init__(self, info_file: UnionIO, mtime_reader: ABCMtimeReader):
        super().__init__(info_file)
        self.mtime_reader = mtime_reader

    @abstractmethod
    def read_infos(self) -> Iterable[Info]:
        'read a list of infos from the info_file'

    def mtime(self) -> datetime:
        return self.mtime_reader.mtime()
