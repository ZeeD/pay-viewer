'xls writer'

from .abcwriter import ABCWriter
import io

from ..model import Info
import typing


class XlsWriter(ABCWriter):
    'write infos on an .xls'

    def write_infos(self,
                    infos: typing.Iterable[Info],
                    info_file: io.RawIOBase
                    ) -> None:
        'write the infos on a file'
        if info_file is None:
            raise Exception('you must pass a file')
        raise NotImplementedError()
