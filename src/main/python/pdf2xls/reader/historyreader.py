'history reader'

from .abcreader import ABCReader
import io
from ..model import Info
import typing


class HistoryReader(ABCReader):
    'retrieve old infos'

    def read_infos(self,
                   info_file: typing.Optional[io.RawIOBase]
                   ) -> typing.Iterable[Info]:
        'read from a file'
        raise NotImplementedError()

    def info_fps(self) -> typing.Iterable[io.RawIOBase]:
        'return a file-like object wrapping an info to import'
        return []  # TODO add history support
