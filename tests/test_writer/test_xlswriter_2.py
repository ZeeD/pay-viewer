from datetime import date
from decimal import Decimal
from unittest import TestCase

from payviewer.model import AdditionalDetail
from payviewer.model import Column
from payviewer.model import ColumnHeader
from payviewer.model import Info
from payviewer.writer.xlswriter import XlsWriter
from testsupport import resource_xls


class TestXlsWriter(TestCase):
    def test_write_zero_rows(self) -> None:
        XlsWriter(resource_xls('testWriteZeroRows')).write_infos([])

    def test_write_one_info_multiple_columns(self) -> None:
        XlsWriter(resource_xls('testWriteOneRow')).write_infos(
            [
                Info(
                    date(2019, 1, 1),
                    [
                        Column(ColumnHeader.minimo, Decimal('1')),
                        Column(ColumnHeader.edr, Decimal('2')),
                    ],
                    [
                        AdditionalDetail(
                            None,
                            None,
                            123,
                            'descr1',
                            Decimal('3'),
                            Decimal('4'),
                            Decimal('5'),
                            Decimal('6'),
                        ),
                        AdditionalDetail(
                            None,
                            None,
                            456,
                            'descr2',
                            Decimal('7'),
                            Decimal('8'),
                            Decimal('9'),
                            Decimal('0'),
                        ),
                    ],
                )
            ]
        )

    def test_write_multiple_infos_different_columns(self) -> None:
        XlsWriter(resource_xls('testWriteOneColumn')).write_infos(
            [
                Info(
                    date(2019, 1, 1),
                    [Column(ColumnHeader.minimo, Decimal('4'))],
                    [],
                ),
                Info(
                    date(2019, 2, 1),
                    [Column(ColumnHeader.edr, Decimal('5'))],
                    [],
                ),
                Info(
                    date(2019, 3, 1),
                    [Column(ColumnHeader.n_scatti, Decimal('6'))],
                    [],
                ),
            ]
        )
