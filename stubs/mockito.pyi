'stub for mockito'

import typing

T = typing.TypeVar('T')


def mock(cls: typing.Type[T]) -> T:
    'mock'


class Mock(typing.Generic[T]):

    def __getattr__(self):
        '---'

    def thenReturn(self) -> None:
        'thenReturn'


def when(obj: T) -> Mock[T]:
    'when'

