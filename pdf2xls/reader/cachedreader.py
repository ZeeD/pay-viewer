'cached reader'

import typing

from . import abcreader
from . import historyreader
from ..model import info
from ..mtime import abcmtimerereader
from ..writer import historywriter


class CachedReader(abcreader.ABCReader):
    'wraps another reader, avoid read_infos if possible'

    def __init__(self,
                 reader: abcreader.ABCReader,
                 info_file: typing.BinaryIO,
                 mtime_reader: abcmtimerereader.ABCMtimeReader,
                 support_reader_class=historyreader.HistoryReader,
                 support_writer_class=historywriter.HistoryWriter):
        super().__init__(info_file, mtime_reader)

        self.reader = reader
        self.support_reader = support_reader_class(info_file, mtime_reader)
        self.support_writer = support_writer_class(info_file, mtime_reader)

    def read_infos(self) -> typing.Iterable[info.Info]:
        'if the cache is fresh, read from it, otherwise update it'

        if self.mtime() < self.reader.mtime():
            infos = self.reader.read_infos()
            self.support_writer.write_feature_infos(None, infos)  # TODO
            return infos

        return self.support_reader.read_infos()
