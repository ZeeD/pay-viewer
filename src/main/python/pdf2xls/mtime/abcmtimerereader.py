'ABC for the mtime readers'

import abc
import datetime
import typing


class ABCMtimeReader(abc.ABC):
    'define an mtime reader'

    def __init__(self, info_file: typing.BinaryIO):
        self.info_file = info_file

    @abc.abstractmethod
    def mtime(self) -> datetime.datetime:
        'retrieve the mtime of the info_file'
