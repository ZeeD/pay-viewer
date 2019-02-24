'history reader'

import datetime
import decimal
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

        ret: typing.Iterable[info.Info] = json.load(info_file,
                                                    object_hook=object_hook)
        return ret


def object_hook(d: typing.Mapping[str, typing.Any]) -> info.Info:
    'create info.Info instances if needed'

    when = datetime.datetime.fromisoformat(d['when'])
    howmuch = decimal.Decimal(d['howmuch'])
    feature = d['feature']
    return info.Info(when, howmuch, feature)
