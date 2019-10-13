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

        ret: typing.Iterable[info.Info] = json.load(self.info_file,
                                                    object_hook=object_hook)
        return ret


def object_hook(d: typing.Mapping[str, typing.Any]) -> info.Info:
    'create info.Info instances if needed'

    when = datetime.date.fromisoformat(d['when'])
    howmuch = decimal.Decimal(d['howmuch'])
    feature = keys.Keys(d['feature'])
    return info.Info(when, howmuch, feature)
