'stub for mockito'

import abc
import typing

T = typing.TypeVar('T')
TT = typing.TypeVar('TT', bound=type)


def mock(spec: typing.Type[T]) -> T:
    'mock'


class Mock(typing.Generic[T]):

    def __getattr__(self, name: str) -> Mock[T]:
        '__getattr__'

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> Mock[T]:
        '__call__'

    def thenReturn(self, *return_values: typing.Any) -> None:
        'thenReturn'


def when(obj: T) -> Mock[T]:
    'when'

