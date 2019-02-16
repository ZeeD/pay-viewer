'test module test_xlswriter'

import datetime
import decimal
import io
import unittest

import pdf2xls.model.info
import pdf2xls.writer.xlswriter


class TestXlsWriter(unittest.TestCase):
    'test class xlswriter.XlsWriter'

    def testReadInfos(self) -> None:
        'history stream is just a json'

        xls_writer = pdf2xls.writer.xlswriter.XlsWriter()
        
        info_file = io.BytesIO()
        feature = 'f'
        infos = [pdf2xls.model.info.Info(datetime.datetime(1982, 5, 11),
                                            decimal.Decimal("1"),
                                            "f")]
        xls_writer.write_feature_infos(info_file, feature, infos)
        info_file.seek(0)
        expected = b''
        actual = info_file.read()

        self.assertEqual(actual, expected)
