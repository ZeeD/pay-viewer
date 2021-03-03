from typing import Iterable, Any
from typing import Iterator
from typing import Protocol
from typing import Tuple
from typing import Union


class At:
    def __getitem__(self, other: Tuple[int, int]) -> Union[str, float]:
        ...


class Iloc:
    def __getitem__(self, other: Tuple[int, int]) -> str:
        ...


class DataFrame:
    at: At
    iloc: Iloc

    def itertuples(self,
                   index: bool=True,
                   name: Optional[str]='Pandas') -> Iterator[Tuple[Any, ...]]:
        ...

    def __getitem__(self, other: int) -> Iterable[float]:
        ...


class Options:
    class Display:
        ...
    display: Options.Display()


options = Options()
