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

MTIME_READER = mockito.mock(
    pdf2xls.mtime.abcmtimerereader.ABCMtimeReader)  # type: ignore


class TestPdfReader(unittest.TestCase):
    'test class test_pdfreader.PdfReader'

    def __init__(self, methodName: str='runTest') -> None:
        super().__init__(methodName)
        self.maxDiff = None

    def testRead201901(self) -> None:
        'testRead201901'

        info_file = loadResourcePdf(2019, 1)
        pdf_reader = pdf2xls.reader.pdfreader.PdfReader(
            info_file, MTIME_READER)
        infos = pdf_reader.read_infos()

        expected = {
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
        }
        self.assertTrue(expected <= set(infos))

    def testRead201208(self) -> None:
        'testRead201208'

        info_file = loadResourcePdf(2012, 8)
        pdf_reader = pdf2xls.reader.pdfreader.PdfReader(
            info_file, MTIME_READER)
        infos = pdf_reader.read_infos()

        expected = {
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
                                    pdf2xls.model.keys.Keys.totale_retributivo),
            pdf2xls.model.info.Info(datetime.date(2012, 8, 1),
                                    decimal.Decimal('255'),
                                    pdf2xls.model.keys.Keys.netto_da_pagare),
            pdf2xls.model.info.Info(datetime.date(2012, 8, 1),
                                    decimal.Decimal('0'),
                                    pdf2xls.model.keys.Keys.ferie_a_prec),
            pdf2xls.model.info.Info(datetime.date(2012, 8, 1),
                                    decimal.Decimal('0'),
                                    pdf2xls.model.keys.Keys.ferie_spett),
            pdf2xls.model.info.Info(datetime.date(2012, 8, 1),
                                    decimal.Decimal('0'),
                                    pdf2xls.model.keys.Keys.ferie_godute),
            pdf2xls.model.info.Info(datetime.date(2012, 8, 1),
                                    decimal.Decimal('0'),
                                    pdf2xls.model.keys.Keys.ferie_saldo),
            pdf2xls.model.info.Info(datetime.date(2012, 8, 1),
                                    decimal.Decimal('0'),
                                    pdf2xls.model.keys.Keys.par_a_prec),
            pdf2xls.model.info.Info(datetime.date(2012, 8, 1),
                                    decimal.Decimal('0'),
                                    pdf2xls.model.keys.Keys.par_spett),
            pdf2xls.model.info.Info(datetime.date(2012, 8, 1),
                                    decimal.Decimal('0'),
                                    pdf2xls.model.keys.Keys.par_godute),
            pdf2xls.model.info.Info(datetime.date(2012, 8, 1),
                                    decimal.Decimal('0'),
                                    pdf2xls.model.keys.Keys.par_saldo)
        }
        self.assertTrue(expected <= set(infos))

    def testRead201213(self) -> None:
        'testRead201213'

        info_file = loadResourcePdf(2012, 13)
        pdf_reader = pdf2xls.reader.pdfreader.PdfReader(
            info_file, MTIME_READER)
        infos = pdf_reader.read_infos()

        expected = {
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
                                    pdf2xls.model.keys.Keys.totale_retributivo),
            pdf2xls.model.info.Info(datetime.date(2012, 12, 31),
                                    decimal.Decimal('402.00'),
                                    pdf2xls.model.keys.Keys.netto_da_pagare),
            pdf2xls.model.info.Info(datetime.date(2012, 12, 31),
                                    decimal.Decimal('0'),
                                    pdf2xls.model.keys.Keys.ferie_a_prec),
            pdf2xls.model.info.Info(datetime.date(2012, 12, 31),
                                    decimal.Decimal('6.68'),
                                    pdf2xls.model.keys.Keys.ferie_spett),
            pdf2xls.model.info.Info(datetime.date(2012, 12, 31),
                                    decimal.Decimal('0'),
                                    pdf2xls.model.keys.Keys.ferie_godute),
            pdf2xls.model.info.Info(datetime.date(2012, 12, 31),
                                    decimal.Decimal('6.68'),
                                    pdf2xls.model.keys.Keys.ferie_saldo),
            pdf2xls.model.info.Info(datetime.date(2012, 12, 31),
                                    decimal.Decimal('0'),
                                    pdf2xls.model.keys.Keys.par_a_prec),
            pdf2xls.model.info.Info(datetime.date(2012, 12, 31),
                                    decimal.Decimal('34.68'),
                                    pdf2xls.model.keys.Keys.par_spett),
            pdf2xls.model.info.Info(datetime.date(2012, 12, 31),
                                    decimal.Decimal('0'),
                                    pdf2xls.model.keys.Keys.par_godute),
            pdf2xls.model.info.Info(datetime.date(2012, 12, 31),
                                    decimal.Decimal('34.68'),
                                    pdf2xls.model.keys.Keys.par_saldo)
        }
        self.assertTrue(expected <= set(infos))

    def test_ferie_godute(self) -> None:
        info_file = loadResourcePdf(2019, 13)
        pdf_reader = pdf2xls.reader.pdfreader.PdfReader(
            info_file, MTIME_READER)
        infos = pdf_reader.read_infos()

        ferie_godute = extract(infos, pdf2xls.model.keys.Keys.ferie_godute)

        self.assertEqual(ferie_godute, decimal.Decimal('3'))

    def test_legenda_2019_01(self) -> None:
        info_file = loadResourcePdf(2019, 1)
        pdf_reader = pdf2xls.reader.pdfreader.PdfReader(
            info_file, MTIME_READER)
        infos = pdf_reader.read_infos()

        legenda_ordinario = extract(
            infos, pdf2xls.model.keys.Keys.legenda_ordinario)
        legenda_ferie = extract(infos, pdf2xls.model.keys.Keys.legenda_ferie)
        legenda_reperibilita = extract(
            infos, pdf2xls.model.keys.Keys.legenda_reperibilita)
        legenda_rol = extract(infos, pdf2xls.model.keys.Keys.legenda_rol)

        self.assertEqual(legenda_ordinario, decimal.Decimal('70'))
        self.assertEqual(legenda_ferie, decimal.Decimal('72'))
        self.assertEqual(legenda_reperibilita, decimal.Decimal('64.5'))
        self.assertEqual(legenda_rol, decimal.Decimal('2'))

    def test_legenda_2017_02(self) -> None:
        info_file = loadResourcePdf(2017, 2)
        pdf_reader = pdf2xls.reader.pdfreader.PdfReader(
            info_file, MTIME_READER)
        infos = pdf_reader.read_infos()

        legenda_ordinario = extract(
            infos, pdf2xls.model.keys.Keys.legenda_ordinario)
        legenda_straordinario = extract(
            infos, pdf2xls.model.keys.Keys.legenda_straordinario)
        legenda_ferie = extract(infos, pdf2xls.model.keys.Keys.legenda_ferie)
        legenda_reperibilita = extract(
            infos, pdf2xls.model.keys.Keys.legenda_reperibilita)
        legenda_rol = extract(infos, pdf2xls.model.keys.Keys.legenda_rol)

        self.assertEqual(legenda_ordinario, decimal.Decimal('136'))
        self.assertEqual(legenda_straordinario, decimal.Decimal('2'))
        self.assertEqual(legenda_ferie, decimal.Decimal('32'))
        self.assertEqual(legenda_reperibilita, decimal.Decimal('102'))
        self.assertEqual(legenda_rol, decimal.Decimal('0'))

    def test_month_2012_09(self) -> None:
        info_file = loadResourcePdf(2012, 9)
        pdf_reader = pdf2xls.reader.pdfreader.PdfReader(info_file,
                                                        MTIME_READER)
        info = next(iter(pdf_reader.read_infos())).when

        self.assertEqual(info, datetime.date(2012, 9, 1))


def extract(infos: typing.Iterable[pdf2xls.model.info.Info],
            key: pdf2xls.model.keys.Keys
            )-> decimal.Decimal:
    return next(info for info in infos if info.feature == key).howmuch
