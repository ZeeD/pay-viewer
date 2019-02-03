'ABC for the writers'

import abc
import io
import typing

from ..model import Info

class ABCWriter(abc.ABC):
    'define a writer'

    def write_infos(self,
                    infos: typing.Iterable[Info],
                    info_file: io.RawIOBase
                    ) -> None:
        'write the infos on a file'
