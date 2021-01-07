'test module xlswriter'

import datetime
import decimal
import unittest

import pdf2xls.model.info
import pdf2xls.model.keys
import pdf2xls.writer.xlswriter

from .. import resourceXls


class TestXlsWriter(unittest.TestCase):
    'test the XlsWriter methods'

    def testWriteZeroRows(self) -> None:
        'read_infos'

        outfile = resourceXls('testWriteZeroRows')

        writer = pdf2xls.writer.xlswriter.XlsWriter(outfile)
        writer.close()

    def testWriteOneRow(self) -> None:
        'read_infos'

        outfile = resourceXls('testWriteOneRow')

        writer = pdf2xls.writer.xlswriter.XlsWriter(outfile)
        writer.write_feature_infos(pdf2xls.model.keys.Keys.minimo, [
            pdf2xls.model.info.InfoPoint(datetime.date(2019, 1, 1),
                                         decimal.Decimal('1'))
        ])
        writer.write_feature_infos(pdf2xls.model.keys.Keys.totale_retributivo, [
            pdf2xls.model.info.InfoPoint(datetime.date(2019, 1, 1),
                                         decimal.Decimal('2'))
        ])
        writer.write_feature_infos(pdf2xls.model.keys.Keys.sup_ass, [
            pdf2xls.model.info.InfoPoint(datetime.date(2019, 1, 1),
                                         decimal.Decimal('2'))
        ])
        writer.close()

    def testWriteOneColumn(self) -> None:
        'read_infos'

        outfile = resourceXls('testWriteOneColumn')

        writer = pdf2xls.writer.xlswriter.XlsWriter(outfile)
        writer.write_feature_infos(pdf2xls.model.keys.Keys.minimo, [
            pdf2xls.model.info.InfoPoint(datetime.date(2019, 1, 1),
                                         decimal.Decimal('1')),
            pdf2xls.model.info.InfoPoint(datetime.date(2019, 2, 1),
                                         decimal.Decimal('2')),
            pdf2xls.model.info.InfoPoint(datetime.date(2019, 3, 1),
                                         decimal.Decimal('3'))
        ])
        writer.close()
