'history reader'

import json
import typing

from . import abcreader
from ..model import info


class HistoryReader(abcreader.ABCReader):
    'retrieve old infos'

    def read_infos(self,
                   info_file: typing.BinaryIO
                   ) -> typing.Iterable[info.Info]:
        'read from a file'

        return json.load(info_file, cls=list)
