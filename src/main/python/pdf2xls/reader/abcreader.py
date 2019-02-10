'ABC for the readers'

import abc
import typing

from ..model import info


class ABCReader(abc.ABC):
    'define a reader'

    @abc.abstractmethod
    def read_infos(self,
                   info_file: typing.BinaryIO
                   ) -> typing.Iterable[info.Info]:
        'read a list of infos from a file'
