'history reader'

from datetime import date
from decimal import Decimal
from json import load
from typing import Iterable
from typing import TextIO

from ..model.info import Info
from ..model.keys import Keys
from ..mtime.abcmtimerereader import ABCMtimeReader
from .abcreader import ABCReader


class HistoryReader(ABCReader):
    'retrieve old infos'

    def __init__(self, info_file: TextIO, mtime_reader: ABCMtimeReader) -> None:
        super().__init__(info_file, mtime_reader)

    def read_infos(self) -> Iterable[Info]:
        'read from a file'

        jsonizable = load(self.info_file)
        table = {date.fromisoformat(k1): {Keys[k2]: (None
                                                     if v2 is None
                                                     else Decimal(v2))
                                          for k2, v2 in v1.items()}
                 for k1, v1 in jsonizable.items()}
        for when, feature_howmuch in table.items():
            for feature, howmuch in feature_howmuch.items():
                yield Info(when, howmuch, feature)
