'history writer'

from json import dump
from typing import TextIO
from typing import cast

from ..model.keys import Keys
from .abcwriter import ABCWriter
from .abcwriter import InfoPoints


class HistoryWriter(ABCWriter):
    'write infos on an .json'

    def __init__(self, info_file: TextIO) -> None:
        super().__init__(info_file)

    def write_feature_infos(self, feature: Keys, infos: InfoPoints) -> None:
        'keep track of the stuff to write'

        for info_point in infos:
            self.table[info_point.when][feature.name] = info_point.howmuch

    def close(self) -> None:
        'atomically write all the infos'

        # convert keys into strings
        jsonizable = {str(k1): {k2: None if v2 is None else str(v2)
                                for k2, v2 in v1.items()}
                      for k1, v1 in self.table.items()}

        dump(jsonizable, cast(TextIO, self.info_file))
        self.info_file.close()
