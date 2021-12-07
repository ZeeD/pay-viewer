from datetime import date
from decimal import Decimal
from unittest import TestCase

from pdf2xls.model import AdditionalDetail
from pdf2xls.model import Column
from pdf2xls.model import ColumnHeader
from pdf2xls.model import Info
from pdf2xls.writer.xlswriter import XlsWriter

from .. import resourceXls


class TestXlsWriter(TestCase):
    'test the XlsWriter methods'

    def testWriteZeroRows(self) -> None:
        XlsWriter(resourceXls('testWriteZeroRows')).write_infos([])

    def testWriteOneInfoMultipleColumns(self) -> None:
        XlsWriter(resourceXls('testWriteOneRow')).write_infos([
            Info(date(2019, 1, 1),
                 [Column(ColumnHeader.minimo, Decimal('1')),
                  Column(ColumnHeader.edr, Decimal('2'))],
                 [AdditionalDetail(None, None, 123, 'descr1', Decimal('3'),
                                   Decimal('4'), Decimal('5'), Decimal('6')),
                  AdditionalDetail(None, None, 456, 'descr2', Decimal('7'),
                                   Decimal('8'), Decimal('9'), Decimal('0')),
                  ])
        ])

    def testWriteMultipleInfosDifferentColumns(self) -> None:
        XlsWriter(resourceXls('testWriteOneColumn')).write_infos([
            Info(date(2019, 1, 1),
                 [Column(ColumnHeader.minimo, Decimal('4'))],
                 []),
            Info(date(2019, 2, 1),
                 [Column(ColumnHeader.edr, Decimal('5'))],
                 []),
            Info(date(2019, 3, 1),
                 [Column(ColumnHeader.n_scatti, Decimal('6'))],
                 [])
        ])
