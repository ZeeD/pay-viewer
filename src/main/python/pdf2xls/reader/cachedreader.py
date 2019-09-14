'cached reader'

import typing

from . import abcreader
from . import historyreader
from ..model import info
from ..mtime import abcmtimerereader
from ..writer import abcwriter
from ..writer import historywriter


class CachedReader(abcreader.ABCReader):
    'wraps another reader, avoid read_infos if possible'

    def __init__(self,
                 reader: abcreader.ABCReader,
                 info_file: typing.TextIO,
                 mtime_reader: abcmtimerereader.ABCMtimeReader,
                 support_reader: typing.Optional[abcreader.ABCReader]=None,
                 support_writer: typing.Optional[abcwriter.ABCWriter]=None
                 ) -> None:
        super().__init__(info_file, mtime_reader)
        self.reader = reader
        if support_reader is not None:
            self.support_reader = support_reader
        else:
            self.support_reader = historyreader.HistoryReader(info_file, mtime_reader)
        if support_writer is not None:
            self.support_writer = support_writer
        else:
            self.support_writer = historywriter.HistoryWriter(info_file)

    def read_infos(self) -> typing.Iterable[info.Info]:
        'if the cache is fresh, read from it, otherwise update it'

        if self.mtime() < self.reader.mtime():
            infos: typing.Iterable[info.Info] = self.reader.read_infos()
            for info_ in infos:
                self.support_writer.write_feature_infos(info_.feature, [info.infoPoint(info_)])
            return infos

        return self.support_reader.read_infos()
