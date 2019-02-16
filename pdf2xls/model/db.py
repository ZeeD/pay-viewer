'''Internal model of the application:

A Db contains all the informations
internally is a dict[ feature, List[ Pair[when, howmuch] ] ]
'''

import collections
import typing

from . import info


class Db:

    def __init__(self):
        self._dict: typing.DefaultDict[str,
                                       typing.List[info.InfoPoint]] = collections.defaultdict(list)

    def add_info(self, info_: info.Info) -> None:
        'add to the internal dict the infos in the info object'
        self._dict[info_.feature].append(info.infoPoint(info_))

    def group_infos_by_feature(self) -> typing.Mapping[str, typing.Iterable[info.InfoPoint]]:
        ret: typing.MutableMapping[str, typing.Iterable[info.InfoPoint]] = {}
        for k in self._dict:
            ret[k] = sorted(self._dict[k])
        return ret
