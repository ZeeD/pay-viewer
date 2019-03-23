'test module test_cachedreader'

import datetime
import decimal
import io
import unittest

import mockito

import pdf2xls.model.info
import pdf2xls.model.keys
import pdf2xls.mtime.abcmtimerereader
import pdf2xls.reader.abcreader
import pdf2xls.reader.cachedreader
import pdf2xls.writer.abcwriter


class TestCachedReader(unittest.TestCase):
    'test class test_cachedreader.TestCachedReader'

    def testReadInfosFromCache(self) -> None:
        'history stream is just a json'

        cached_infos = [pdf2xls.model.info.Info(datetime.date(1982, 5, 11),
                                            decimal.Decimal("1"),
                                            pdf2xls.model.keys.Keys.minimo)]

        mock_reader = mockito.mock(pdf2xls.reader.abcreader.ABCReader)
        info_file = io.BytesIO(
            b'[{"when":"1982-05-11","howmuch":1,"feature":4}]')
        mock_mtime_reader = mockito.mock(pdf2xls.mtime.abcmtimerereader.ABCMtimeReader)
        mock_support_reader = mockito.mock(pdf2xls.reader.abcreader.ABCReader)
        mock_support_writer = mockito.mock(pdf2xls.writer.abcwriter.ABCWriter)

        mockito.when(mock_mtime_reader).mtime().thenReturn(datetime.datetime(1983, 11, 10))
        mockito.when(mock_reader).mtime().thenReturn(datetime.datetime(1982, 5, 11))
        mockito.when(mock_support_reader).read_infos().thenReturn(cached_infos)

        cached_reader = pdf2xls.reader.cachedreader.CachedReader(
            mock_reader,
            info_file, mock_mtime_reader,
            mock_support_reader,
            mock_support_writer)

        expected = cached_infos
        infos = cached_reader.read_infos()
        self.assertEqual(infos, expected)
