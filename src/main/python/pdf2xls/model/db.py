'''Internal model of the application:

A Db contains all the informations
internally is a dict[ feature, List[ Pair[when, howmuch] ] ]
'''

import collections
import typing

from . import info
from . import keys

DD_T = typing.DefaultDict[keys.Keys, typing.List[info.InfoPoint]]
M_T = typing.Mapping[keys.Keys, typing.Iterable[info.InfoPoint]]
MM_T = typing.MutableMapping[keys.Keys, typing.Iterable[info.InfoPoint]]


class Db:

    def __init__(self) -> None:
        self._dict: DD_T = collections.defaultdict(list)

    def add_info(self, info_: info.Info) -> None:
        'add to the internal dict the infos in the info object'
        self._dict[info_.feature].append(info.infoPoint(info_))

    def group_infos_by_feature(self) -> M_T:
        ret: MM_T = {}
        for k in self._dict:
            ret[k] = sorted(self._dict[k])
        return ret
