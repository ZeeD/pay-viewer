'mtime reader'

import datetime
import os

from . import abcmtimerereader


class MtimeReader(abcmtimerereader.ABCMtimeReader):
    'retrieve mtime'

    def mtime(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(
            os.path.getmtime(self.info_file.name))
