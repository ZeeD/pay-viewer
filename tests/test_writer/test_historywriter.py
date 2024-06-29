from datetime import date
from decimal import Decimal
from pathlib import Path
from unittest import TestCase
from unittest.mock import mock_open
from unittest.mock import patch

from payviewer.model import Column
from payviewer.model import ColumnHeader
from payviewer.model import Info
from payviewer.writer.historywriter import HistoryWriter


class TestHistoryWriter(TestCase):
    def test_write_infos(self) -> None:
        mock = mock_open()
        with patch('pathlib.io.open', mock):
            HistoryWriter(Path()).write_infos(
                [
                    Info(
                        date(1982, 5, 11),
                        [Column(ColumnHeader.minimo, Decimal('1'))],
                        [],
                    )
                ]
            )

        mock().write.assert_called()
