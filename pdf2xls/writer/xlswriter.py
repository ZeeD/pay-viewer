'xls writer'

import typing

from . import abcwriter
from ..model import info


class XlsWriter(abcwriter.ABCWriter):
    'write infos on an .xls'

    def write_feature_infos(self,
                            info_file: typing.BinaryIO,
                            feature: str,
                            infos: typing.Iterable[info.InfoPoint]) -> None:
        'write the infos on a file'
        raise NotImplementedError()
