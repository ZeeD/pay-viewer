'test module test_pdfreader'

import datetime
import decimal
import typing
import unittest

import mockito

import pdf2xls.model.info
import pdf2xls.model.keys
import pdf2xls.mtime.abcmtimerereader
import pdf2xls.reader.pdfreader

from .. import loadResourcePdf


class TestPdfReader(unittest.TestCase):
    'test class test_pdfreader.PdfReader'

    def testRead201901(self) -> None:
        'testRead201901'

        info_file = loadResourcePdf(2019, 1)
        mock_mtime_reader = mockito.mock(pdf2xls.mtime.abcmtimerereader.ABCMtimeReader)
        pdf_reader = pdf2xls.reader.pdfreader.PdfReader(info_file, mock_mtime_reader)
        infos = pdf_reader.read_infos()

        expected = [
            pdf2xls.model.info.Info(datetime.date(2019, 1, 1),
                                    decimal.Decimal('2061.41'),
                                    pdf2xls.model.keys.Keys.minimo),
            pdf2xls.model.info.Info(datetime.date(2019, 1, 1),
                                    decimal.Decimal('109.23'),
                                    pdf2xls.model.keys.Keys.scatti),
            pdf2xls.model.info.Info(datetime.date(2019, 1, 1),
                                    decimal.Decimal('50.87'),
                                    pdf2xls.model.keys.Keys.superm),
            pdf2xls.model.info.Info(datetime.date(2019, 1, 1),
                                    decimal.Decimal('674.16'),
                                    pdf2xls.model.keys.Keys.sup_ass),
            pdf2xls.model.info.Info(datetime.date(2019, 1, 1),
                                    decimal.Decimal('0'),
                                    pdf2xls.model.keys.Keys.edr),
            pdf2xls.model.info.Info(datetime.date(2019, 1, 1),
                                    decimal.Decimal('2895.67'),
                                    pdf2xls.model.keys.Keys.totale_retributivo)
        ]
        self.assertEqual(infos, expected)

    def testRead201208(self) -> None:
        'testRead201208'

        info_file = loadResourcePdf(2012, 8)
        mock_mtime_reader = mockito.mock(pdf2xls.mtime.abcmtimerereader.ABCMtimeReader)
        pdf_reader = pdf2xls.reader.pdfreader.PdfReader(info_file, mock_mtime_reader)
        infos = pdf_reader.read_infos()

        expected = [
            pdf2xls.model.info.Info(datetime.date(2012, 8, 1),
                                    decimal.Decimal('1634.56'),
                                    pdf2xls.model.keys.Keys.minimo),
            pdf2xls.model.info.Info(datetime.date(2012, 8, 1),
                                    decimal.Decimal('0'),
                                    pdf2xls.model.keys.Keys.scatti),
            pdf2xls.model.info.Info(datetime.date(2012, 8, 1),
                                    decimal.Decimal('0'),
                                    pdf2xls.model.keys.Keys.superm),
            pdf2xls.model.info.Info(datetime.date(2012, 8, 1),
                                    decimal.Decimal('85.87'),
                                    pdf2xls.model.keys.Keys.sup_ass),
            pdf2xls.model.info.Info(datetime.date(2012, 8, 1),
                                    decimal.Decimal('10.33'),
                                    pdf2xls.model.keys.Keys.edr),
            pdf2xls.model.info.Info(datetime.date(2012, 8, 1),
                                    decimal.Decimal('1730.76'),
                                    pdf2xls.model.keys.Keys.totale_retributivo)
        ]
        self.assertEqual(infos, expected)

    def testRead201213(self) -> None:
        'testRead201213'

        info_file = loadResourcePdf(2012, 13)
        mock_mtime_reader = mockito.mock(pdf2xls.mtime.abcmtimerereader.ABCMtimeReader)
        pdf_reader = pdf2xls.reader.pdfreader.PdfReader(info_file, mock_mtime_reader)
        infos = pdf_reader.read_infos()

        expected = [
            pdf2xls.model.info.Info(datetime.date(2012, 12, 31),
                                    decimal.Decimal('1634.56'),
                                    pdf2xls.model.keys.Keys.minimo),
            pdf2xls.model.info.Info(datetime.date(2012, 12, 31),
                                    decimal.Decimal('0'),
                                    pdf2xls.model.keys.Keys.scatti),
            pdf2xls.model.info.Info(datetime.date(2012, 12, 31),
                                    decimal.Decimal('0'),
                                    pdf2xls.model.keys.Keys.superm),
            pdf2xls.model.info.Info(datetime.date(2012, 12, 31),
                                    decimal.Decimal('85.87'),
                                    pdf2xls.model.keys.Keys.sup_ass),
            pdf2xls.model.info.Info(datetime.date(2012, 12, 31),
                                    decimal.Decimal('10.33'),
                                    pdf2xls.model.keys.Keys.edr),
            pdf2xls.model.info.Info(datetime.date(2012, 12, 31),
                                    decimal.Decimal('1730.76'),
                                    pdf2xls.model.keys.Keys.totale_retributivo)
        ]
        self.assertEqual(infos, expected)
