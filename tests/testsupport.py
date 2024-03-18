from contextlib import contextmanager
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Final
from unittest.mock import MagicMock
from unittest.mock import patch

if TYPE_CHECKING:
    from collections.abc import Iterator


@contextmanager
def stub_open(content: str) -> 'Iterator[MagicMock]':
    with patch.object(Path, 'open') as mock:
        mock.return_value = StringIO(content)
        yield mock


_RESOURCES: Final = Path(__file__).parent / 'resources'


def resource_pdf(year: int, month: int) -> Path:
    return _RESOURCES / f'{year:04}' / f'Cedolini_{year:04}_{month:02}.pdf'


def resource_xls(filename: str) -> Path:
    return _RESOURCES / 'outxls' / f'{filename}.xlsx'
