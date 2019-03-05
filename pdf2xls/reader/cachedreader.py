'cached reader'

import datetime
import decimal
import json
import typing

from . import abcreader
from . import historyreader
from ..model import info
from ..model import keys
from ..writer import historywriter


class CachedReader(abcreader.ABCReader):
    'wraps another reader, avoid read_infos if possible'
    
    def __init__(self,
                 reader: abcreader.ABCReader,
                 support_reader=historyreader.HistoryReader(),
                 support_writer=historywriter.HistoryWriter()):
        self.reader = reader
        self.support_reader = support_reader
        self.support_writer = support_writer

    def read_infos(self,
                   info_file: typing.BinaryIO
                   ) -> typing.Iterable[info.Info]:
        'read from a file'

        ret: typing.Iterable[info.Info] = json.load(info_file,
                                                    object_hook=object_hook)
        return ret


def object_hook(d: typing.Mapping[str, typing.Any]) -> info.Info:
    'create info.Info instances if needed'

    when = datetime.date.fromisoformat(d['when'])
    howmuch = decimal.Decimal(d['howmuch'])
    feature = keys.Keys(d['feature'])
    return info.Info(when, howmuch, feature)
