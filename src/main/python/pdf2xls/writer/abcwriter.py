'ABC for the writers'

import abc
import typing

from ..model import info
from ..model import keys
from ..mtime import abcmtimerereader


class ABCWriter(abc.ABC):
    'define a writer'

    def __init__(self,
                 info_file: abcmtimerereader.UnionIO) -> None:
        'keep track of the info_file'
        self.info_file = info_file

    @abc.abstractmethod
    def write_feature_infos(self,
                            feature: keys.Keys,
                            infos: typing.Iterable[info.InfoPoint]
                            ) -> None:
        'append an info to a file - returns mtime'

    @abc.abstractmethod
    def close(self) -> None:
        'close the info_file'

    @classmethod
    def __class_getitem__(cls) -> None:
        'make pylint happy'
        ...
