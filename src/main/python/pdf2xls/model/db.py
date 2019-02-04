'''Internal model of the application:

A Db contains all the informations
internally is a dict[ feature, List[ Pair[when, howmuch] ] ]
'''

import collections
import datetime
import decimal
import typing

from .info import Info


class Db:

    def __init__(self):
        self._dict: typing.DefaultDict[str,
                                       typing.List[(datetime.datetime,
                                                    decimal.Decimal)]] = None
        self._dict = collections.defaultdict(list)

    def read_info(self, info: Info) -> None:
        'add to the internal dict the infos in the info object'
        self._dict[info.feature].append((info.when, info.howmuch))
