from contextlib import contextmanager
from pathlib import Path
from typing import Iterator
from unittest.mock import MagicMock
from unittest.mock import mock_open
from unittest.mock import patch


@contextmanager
def stub_open(content: str) -> Iterator[MagicMock]:
    with patch('builtins.open', mock_open(read_data=content)) as mock:
        yield mock


def loadResourcePdf(year: int, month: int) -> str:
    'load a pdf from the resources path'
    here = Path(__file__).parent
    p = here / '..' / 'resources' / f'{year:04}' / f'Cedolini_{year:04}_{month:02}.pdf'
    return str(p)


def resourceXls(filename: str) -> str:
    'open a writable file to a xls from the resources path'
    here = Path(__file__).parent
    p = here / '..' / 'resources' / 'outxls' / f'{filename}.xlsx'
    return str(p)
