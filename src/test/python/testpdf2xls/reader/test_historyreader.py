'test module test_historyreader'

import datetime
import decimal
import io
import unittest

import mockito

import pdf2xls.model.info
import pdf2xls.model.keys
import pdf2xls.mtime.abcmtimerereader
import pdf2xls.reader.historyreader


class TestHistoryReader(unittest.TestCase):
    'test class test_historyreader.HistoryReader'

    def testReadInfos(self) -> None:
        'history stream is just a json'

        expected = [pdf2xls.model.info.Info(datetime.date(1982, 5, 11),
                                            decimal.Decimal("1"),
                                            pdf2xls.model.keys.Keys.minimo)]

        info_file = io.StringIO('[{"when":"1982-05-11","howmuch":1,"feature":4}]')
        mock_mtime_reader = mockito.mock(pdf2xls.mtime.abcmtimerereader.ABCMtimeReader)  # type: ignore
        history_reader = pdf2xls.reader.historyreader.HistoryReader(info_file, mock_mtime_reader)
        infos = history_reader.read_infos()
        self.assertEqual(infos, expected)
