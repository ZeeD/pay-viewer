from contextlib import contextmanager
from typing import Iterator
from unittest.mock import MagicMock
from unittest.mock import mock_open
from unittest.mock import patch


@contextmanager
def stub_open(content: str) -> Iterator[MagicMock]:
    with patch('builtins.open', mock_open(read_data=content)) as mock:
        print(type(mock))
        yield mock
