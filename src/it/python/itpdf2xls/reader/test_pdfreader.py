'test module test_pdfreader'

from datetime import date
from decimal import Decimal
from typing import Iterable
from typing import Optional
from unittest import TestCase

from mockito import mock

from pdf2xls.model.info import Info
from pdf2xls.model.keys import ColumnHeader
from pdf2xls.mtime.abcmtimerereader import ABCMtimeReader
from pdf2xls.reader.pdfreader import PdfReader

from .. import loadResourcePdf

MTIME_READER = mock(ABCMtimeReader)  # type: ignore


class TestPdfReader(TestCase):
    'test class test_pdfreader.PdfReader'

    def __init__(self, methodName: str='runTest') -> None:
        super().__init__(methodName)
        self.maxDiff = None

    def testRead201901(self) -> None:
        'testRead201901'

        info_file = loadResourcePdf(2019, 1)
        pdf_reader = PdfReader(info_file, MTIME_READER)
        infos = pdf_reader.read_infos()

        expected = {Info(date(2019, 1, 1), Decimal('2061.41'), ColumnHeader.minimo),
                    Info(date(2019, 1, 1), Decimal('109.23'), ColumnHeader.scatti),
                    Info(date(2019, 1, 1), Decimal('50.87'), ColumnHeader.superm),
                    Info(date(2019, 1, 1), Decimal('674.16'), ColumnHeader.sup_ass),
                    Info(date(2019, 1, 1), Decimal('0'), ColumnHeader.edr),
                    Info(date(2019, 1, 1), Decimal('2895.67'), ColumnHeader.totale_retributivo)}
        self.assertTrue(expected <= set(infos))

    def testRead201208(self) -> None:
        'testRead201208'

        info_file = loadResourcePdf(2012, 8)
        pdf_reader = PdfReader(info_file, MTIME_READER)
        infos = pdf_reader.read_infos()

        expected = {Info(date(2012, 8, 1), Decimal('1634.56'), ColumnHeader.minimo),
                    Info(date(2012, 8, 1), Decimal('0'), ColumnHeader.scatti),
                    Info(date(2012, 8, 1), Decimal('0'), ColumnHeader.superm),
                    Info(date(2012, 8, 1), Decimal('85.87'), ColumnHeader.sup_ass),
                    Info(date(2012, 8, 1), Decimal('10.33'), ColumnHeader.edr),
                    Info(date(2012, 8, 1), Decimal('1730.76'),
                         ColumnHeader.totale_retributivo),
                    Info(date(2012, 8, 1), Decimal('255'),
                         ColumnHeader.netto_da_pagare),
                    Info(date(2012, 8, 1), Decimal('0'), ColumnHeader.ferie_a_prec),
                    Info(date(2012, 8, 1), Decimal('0'), ColumnHeader.ferie_spett),
                    Info(date(2012, 8, 1), Decimal('0'), ColumnHeader.ferie_godute),
                    Info(date(2012, 8, 1), Decimal('0'), ColumnHeader.ferie_saldo),
                    Info(date(2012, 8, 1), Decimal('0'), ColumnHeader.par_a_prec),
                    Info(date(2012, 8, 1), Decimal('0'), ColumnHeader.par_spett),
                    Info(date(2012, 8, 1), Decimal('0'), ColumnHeader.par_godute),
                    Info(date(2012, 8, 1), Decimal('0'), ColumnHeader.par_saldo)}
        self.assertTrue(expected <= set(infos))

    def testRead201213(self) -> None:
        'testRead201213'

        info_file = loadResourcePdf(2012, 13)
        pdf_reader = PdfReader(info_file, MTIME_READER)
        infos = pdf_reader.read_infos()

        expected = {Info(date(2012, 12, 31), Decimal('1634.56'), ColumnHeader.minimo),
                    Info(date(2012, 12, 31), Decimal('0'), ColumnHeader.scatti),
                    Info(date(2012, 12, 31), Decimal('0'), ColumnHeader.superm),
                    Info(date(2012, 12, 31), Decimal('85.87'), ColumnHeader.sup_ass),
                    Info(date(2012, 12, 31), Decimal('10.33'), ColumnHeader.edr),
                    Info(date(2012, 12, 31), Decimal('1730.76'),
                         ColumnHeader.totale_retributivo),
                    Info(date(2012, 12, 31), Decimal('402.00'),
                         ColumnHeader.netto_da_pagare),
                    Info(date(2012, 12, 31), Decimal('0'), ColumnHeader.ferie_a_prec),
                    Info(date(2012, 12, 31), Decimal('6.68'),
                         ColumnHeader.ferie_spett),
                    Info(date(2012, 12, 31), Decimal('0'), ColumnHeader.ferie_godute),
                    Info(date(2012, 12, 31), Decimal('6.68'),
                         ColumnHeader.ferie_saldo),
                    Info(date(2012, 12, 31), Decimal('0'), ColumnHeader.par_a_prec),
                    Info(date(2012, 12, 31), Decimal('34.68'), ColumnHeader.par_spett),
                    Info(date(2012, 12, 31), Decimal('0'), ColumnHeader.par_godute),
                    Info(date(2012, 12, 31), Decimal('34.68'), ColumnHeader.par_saldo)}
        self.assertTrue(expected <= set(infos))

    def test_ferie_godute(self) -> None:
        info_file = loadResourcePdf(2019, 13)
        pdf_reader = PdfReader(info_file, MTIME_READER)
        infos = pdf_reader.read_infos()

        ferie_godute = extract(infos, ColumnHeader.ferie_godute)

        self.assertEqual(ferie_godute, Decimal('3'))

    def test_legenda_2019_01(self) -> None:
        info_file = loadResourcePdf(2019, 1)
        pdf_reader = PdfReader(info_file, MTIME_READER)
        infos = pdf_reader.read_infos()

        legenda_ordinario = extract(infos, ColumnHeader.legenda_ordinario)
        legenda_ferie = extract(infos, ColumnHeader.legenda_ferie)
        legenda_reperibilita = extract(infos, ColumnHeader.legenda_reperibilita)
        legenda_rol = extract(infos, ColumnHeader.legenda_rol)

        self.assertEqual(legenda_ordinario, Decimal('70'))
        self.assertEqual(legenda_ferie, Decimal('72'))
        self.assertEqual(legenda_reperibilita, Decimal('64.5'))
        self.assertEqual(legenda_rol, Decimal('2'))

    def test_legenda_2017_02(self) -> None:
        info_file = loadResourcePdf(2017, 2)
        pdf_reader = PdfReader(info_file, MTIME_READER)
        infos = pdf_reader.read_infos()

        legenda_ordinario = extract(infos, ColumnHeader.legenda_ordinario)
        legenda_straordinario = extract(infos, ColumnHeader.legenda_straordinario)
        legenda_ferie = extract(infos, ColumnHeader.legenda_ferie)
        legenda_reperibilita = extract(infos, ColumnHeader.legenda_reperibilita)
        legenda_rol = extract(infos, ColumnHeader.legenda_rol)

        self.assertEqual(legenda_ordinario, Decimal('136'))
        self.assertEqual(legenda_straordinario, Decimal('2'))
        self.assertEqual(legenda_ferie, Decimal('32'))
        self.assertEqual(legenda_reperibilita, Decimal('102'))
        self.assertEqual(legenda_rol, Decimal('0'))

    def test_month_2012_09(self) -> None:
        info_file = loadResourcePdf(2012, 9)
        pdf_reader = PdfReader(info_file, MTIME_READER)
        info = next(iter(pdf_reader.read_infos())).when

        self.assertEqual(info, date(2012, 9, 1))


def extract(infos: Iterable[Info], key: ColumnHeader)-> Optional[Decimal]:
    return next(info for info in infos if info.header == key).howmuch
