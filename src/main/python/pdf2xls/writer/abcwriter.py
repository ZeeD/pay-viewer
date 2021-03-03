'ABC for the writers'

from abc import ABC
from abc import abstractmethod
from collections import defaultdict
from datetime import date
from decimal import Decimal
from typing import DefaultDict
from typing import Dict
from typing import Iterable
from typing import Optional

from ..model.info import InfoPoint
from ..model.keys import Keys
from ..mtime.abcmtimerereader import UnionIO

Table = DefaultDict[date, Dict[str, Optional[Decimal]]]
InfoPoints = Iterable[InfoPoint]

class ABCWriter(ABC):
    'define a writer'

    def __init__(self, info_file: UnionIO) -> None:
        'keep track of the info_file'
        self.info_file = info_file
        # by month, then by key
        self.table: Table = defaultdict(dict)

    @abstractmethod
    def write_feature_infos(self, feature: Keys, infos: InfoPoints) -> None:
        'append an info to a file - returns mtime'

    @abstractmethod
    def close(self) -> None:
        'close the info_file'

    @classmethod
    def __class_getitem__(cls) -> None:
        'make pylint happy'
