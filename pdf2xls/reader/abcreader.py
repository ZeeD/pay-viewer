'ABC for the readers'

import abc
import datetime
import typing

from ..model import info
from ..mtime import abcmtimerereader


class ABCReader(abcmtimerereader.ABCMtimeReader):
    'define a reader'

    def __init__(self,
                 info_file: typing.BinaryIO,
                 mtime_reader: abcmtimerereader.ABCMtimeReader):
        self.info_file = info_file
        self.mtime_reader = mtime_reader

    @abc.abstractmethod
    def read_infos(self) -> typing.Iterable[info.Info]:
        'read a list of infos from the info_file'

    def mtime(self) -> datetime.datetime:
        return self.mtime_reader.mtime()
