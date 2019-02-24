'test module test_pdfreader'

import datetime
import decimal
import unittest

import pdf2xls.model.info
import pdf2xls.model.keys
import pdf2xls.reader.pdfreader

from .. import loadResourcePdf


class TestPdfReader(unittest.TestCase):
    'test class test_pdfreader.PdfReader'

    def testReadInfosRealPdf(self) -> None:
        'history stream is a pdf full of stuff'

        pdf_reader = pdf2xls.reader.pdfreader.PdfReader()
        info_file = loadResourcePdf(2019, 1)

        expected = [
            pdf2xls.model.info.Info(datetime.datetime(2019, 1, 1),
                                    decimal.Decimal('2061.41'),
                                    pdf2xls.model.keys.Keys.minimo),
            pdf2xls.model.info.Info(datetime.datetime(2019, 1, 1),
                                    decimal.Decimal('109.23'),
                                    pdf2xls.model.keys.Keys.scatti),
            pdf2xls.model.info.Info(datetime.datetime(2019, 1, 1),
                                    decimal.Decimal('50.87'),
                                    pdf2xls.model.keys.Keys.superm),
            pdf2xls.model.info.Info(datetime.datetime(2019, 1, 1),
                                    decimal.Decimal('674.16'),
                                    pdf2xls.model.keys.Keys.sup_ass),
            pdf2xls.model.info.Info(datetime.datetime(2019, 1, 1),
                                    decimal.Decimal('2895.67'),
                                    pdf2xls.model.keys.Keys.totale_retributivo)
        ]
        infos = pdf_reader.read_infos(info_file)
        self.assertEqual(infos, expected)
