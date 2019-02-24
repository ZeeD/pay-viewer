'ABC for the writers'

import abc
import typing

from ..model import info
from ..model import keys


class ABCWriter(abc.ABC):
    'define a writer'

    @abc.abstractmethod
    def write_feature_infos(self,
                            info_file: typing.BinaryIO,
                            feature: keys.Keys,
                            infos: typing.Iterable[info.InfoPoint]
                            ) -> None:
        'append an info to a file'
