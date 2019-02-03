'ABC for the readers'

import abc
import io
import typing

from ..model import Info

class ABCReader(abc.ABC):
    'define a reader'

    def read_infos(self,
                   info_file: typing.Optional[io.RawIOBase]
                   ) -> typing.Iterable[Info]:
        'read a list of infos from a file'
