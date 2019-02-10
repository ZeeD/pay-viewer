'ABC for the writers'

import abc
import typing

from ..model import info


class ABCWriter(abc.ABC):
    'define a writer'

    @abc.abstractmethod
    def write_feature_infos(self,
                            info_file: typing.BinaryIO,
                            feature: str,
                            infos: typing.Iterable[info.InfoPoint]
                            ) -> None:
        'append an info to a file'
