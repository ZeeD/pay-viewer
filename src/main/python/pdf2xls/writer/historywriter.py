'history writer'

import collections
import json
import typing

from . import abcwriter
from . import xlswriter
from ..model import info
from ..model import keys


class HistoryWriter(abcwriter.ABCWriter[typing.TextIO]):
    'write infos on an .json'

    def __init__(self,
                 info_file: typing.TextIO) -> None:
        super().__init__(info_file)
        self.table: xlswriter.TABLE_T = collections.defaultdict(dict)  # by month, then by key

    def write_feature_infos(self,
                            feature: keys.Keys,
                            infos: typing.Iterable[info.InfoPoint]) -> None:
        'keep track of the stuff to write'

        for ip in infos:
            self.table[ip.when][feature.name] = ip.howmuch

    def close(self) -> None:
        'atomically write all the infos'

        json.dump(self.table, self.info_file)
