'history writer'

import json
import typing

from . import abcwriter
from ..model import info
from ..model import keys


class HistoryWriter(abcwriter.ABCWriter):
    'write infos on an .json'

    def __init__(self,
                 info_file: typing.TextIO
                 ) -> None:
        super().__init__(info_file)

    def write_feature_infos(self,
                            feature: keys.Keys,
                            infos: typing.Iterable[info.InfoPoint]) -> None:
        'keep track of the stuff to write'

        for info_point in infos:
            self.table[info_point.when][feature.name] = info_point.howmuch

    def close(self) -> None:
        'atomically write all the infos'

        # convert keys into strings
        jsonizable = {
            str(k1): {
                k2: str(v2)
                for k2, v2 in v1.items()
            }
            for k1, v1 in self.table.items()
        }

        json.dump(jsonizable, typing.cast(typing.TextIO, self.info_file))
        self.info_file.close()
