'test module history_xlswriter'

import datetime
import decimal
import io
import unittest

import pdf2xls.model.info
import pdf2xls.model.keys
import pdf2xls.writer.xlswriter


class TestHistoryWriter(unittest.TestCase):
    'test class historywriter.HistoryWriter'

    def testWriteInfos(self) -> None:
        'testWriteInfos'

        info_file = io.BytesIO()

        feature = pdf2xls.model.keys.ColumnHeader.minimo
        infos = [pdf2xls.model.info.InfoPoint(datetime.date(1982, 5, 11),
                                              decimal.Decimal("1"))]

        xls_writer = pdf2xls.writer.xlswriter.XlsWriter(info_file)
        xls_writer.write_feature_infos(feature, infos)
        xls_writer.close()

        info_file.seek(0)
        actual = info_file.read()

        self.assertTrue(actual is not None)
