'test module test_historyreader'

import datetime
import decimal
import io
import unittest

import pdf2xls.model.info
import pdf2xls.reader.historyreader


class TestHistoryReader(unittest.TestCase):
    'test class test_historyreader.HistoryReader'

    def testReadInfos(self) -> None:
        'history stream is just a json'

        history_reader = pdf2xls.reader.historyreader.HistoryReader()
        info_file = io.BytesIO(
            b'[{"when":"1982-05-11","howmuch":1,"feature":"f"}]')

        expected = [pdf2xls.model.info.Info(datetime.datetime(1982, 5, 11),
                                            decimal.Decimal("1"),
                                            "f")]
        infos = history_reader.read_infos(info_file)
        self.assertEqual(infos, expected)
