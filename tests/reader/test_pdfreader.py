'test module test_pdfreader'

import datetime
import decimal
import unittest

import pdf2xls.model.info
import pdf2xls.reader.pdfreader

from .. import loadResourcePdf


class TestPdfReader(unittest.TestCase):
    'test class test_pdfreader.PdfReader'

    def testReadInfos(self) -> None:
        'history stream is a pdf full of stuff'

        pdf_reader = pdf2xls.reader.pdfreader.PdfReader()
        info_file = loadResourcePdf(2019, 1)

        expected = [pdf2xls.model.info.Info(datetime.datetime(1982, 5, 11),
                                            decimal.Decimal("1"),
                                            "f")]
        infos = pdf_reader.read_infos(info_file)
        self.assertEqual(infos, expected)
