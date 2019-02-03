'pdf reader'

from .abcreader import ABCReader
import io

from ..model import Info
import typing


class PdfReader(ABCReader):
    'retrieve infos from .pdf'

    def read_infos(self,
                   info_file: typing.Optional[io.RawIOBase]
                   ) -> typing.Iterable[Info]:
        'read from a file'
        if info_file is None:
            raise Exception('you must pass a file')
        raise NotImplementedError()
