'history reader'

import datetime
import decimal
import json
import typing

from . import abcreader
from ..model import info
from ..model import keys
from ..mtime import abcmtimerereader


class HistoryReader(abcreader.ABCReader):
    'retrieve old infos'

    def __init__(self,
                 info_file: typing.TextIO,
                 mtime_reader: abcmtimerereader.ABCMtimeReader):
        super().__init__(info_file, mtime_reader)

    def read_infos(self) -> typing.Iterable[info.Info]:
        'read from a file'

        jsonizable = json.load(self.info_file)
        table = {
            datetime.date.fromisoformat(k1): {
                keys.Keys[k2]: decimal.Decimal(v2)
                for k2, v2 in v1.items()
            }
            for k1, v1 in jsonizable.items()
        }
        for when, feature_howmuch in table.items():
            for feature, howmuch in feature_howmuch.items():
                yield info.Info(when, howmuch, feature)
