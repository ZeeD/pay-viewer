from datetime import date
from decimal import Decimal
from unittest import TestCase

from payviewer.model import Column
from payviewer.model import ColumnHeader
from payviewer.model import Info
from payviewer.reader.pdfreader import PdfReader
from testsupport import resource_pdf


class TestPdfReader(TestCase):
    maxDiff = None

    def test_read_2019_01(self) -> None:
        [info] = PdfReader(resource_pdf(2019, 1)).read_infos()
        self.assertEqual(date(2019, 1, 1), info.when)
        actual = set(info.columns)

        expected = {
            Column(ColumnHeader.minimo, Decimal('2061.41')),
            Column(ColumnHeader.scatti, Decimal('109.23')),
            Column(ColumnHeader.superm, Decimal('50.87')),
            Column(ColumnHeader.sup_ass, Decimal('674.16')),
            Column(ColumnHeader.edr, Decimal(0)),
            Column(ColumnHeader.totale_retributivo, Decimal('2895.67')),
        }
        self.assertTrue(expected <= actual)

    def test_read_2012_08(self) -> None:
        [info] = PdfReader(resource_pdf(2012, 8)).read_infos()
        self.assertEqual(date(2012, 8, 1), info.when)
        actual = set(info.columns)

        expected = {
            Column(ColumnHeader.minimo, Decimal('1634.56')),
            Column(ColumnHeader.scatti, Decimal(0)),
            Column(ColumnHeader.superm, Decimal(0)),
            Column(ColumnHeader.sup_ass, Decimal('85.87')),
            Column(ColumnHeader.edr, Decimal('10.33')),
            Column(ColumnHeader.totale_retributivo, Decimal('1730.76')),
            Column(ColumnHeader.netto_da_pagare, Decimal(255)),
            Column(ColumnHeader.ferie_a_prec, Decimal(0)),
            Column(ColumnHeader.ferie_spett, Decimal(0)),
            Column(ColumnHeader.ferie_godute, Decimal(0)),
            Column(ColumnHeader.ferie_saldo, Decimal(0)),
            Column(ColumnHeader.par_a_prec, Decimal(0)),
            Column(ColumnHeader.par_spett, Decimal(0)),
            Column(ColumnHeader.par_godute, Decimal(0)),
            Column(ColumnHeader.par_saldo, Decimal(0)),
        }
        self.assertTrue(expected <= actual)

    def test_read_2012_13(self) -> None:
        [info] = PdfReader(resource_pdf(2012, 13)).read_infos()
        self.assertEqual(date(2012, 12, 31), info.when)
        actual = set(info.columns)

        expected = {
            Column(ColumnHeader.minimo, Decimal('1634.56')),
            Column(ColumnHeader.scatti, Decimal(0)),
            Column(ColumnHeader.superm, Decimal(0)),
            Column(ColumnHeader.sup_ass, Decimal('85.87')),
            Column(ColumnHeader.edr, Decimal('10.33')),
            Column(ColumnHeader.totale_retributivo, Decimal('1730.76')),
            Column(ColumnHeader.netto_da_pagare, Decimal('402.00')),
            Column(ColumnHeader.ferie_a_prec, Decimal(0)),
            Column(ColumnHeader.ferie_spett, Decimal('6.68')),
            Column(ColumnHeader.ferie_godute, Decimal(0)),
            Column(ColumnHeader.ferie_saldo, Decimal('6.68')),
            Column(ColumnHeader.par_a_prec, Decimal(0)),
            Column(ColumnHeader.par_spett, Decimal('34.68')),
            Column(ColumnHeader.par_godute, Decimal(0)),
            Column(ColumnHeader.par_saldo, Decimal('34.68')),
        }
        self.assertTrue(expected <= actual)

    def test_ferie_godute(self) -> None:
        infos = PdfReader(resource_pdf(2019, 13)).read_infos()

        ferie_godute = extract(infos, ColumnHeader.ferie_godute)
        self.assertEqual(ferie_godute, Decimal(3))

    def test_legenda_2019_01(self) -> None:
        infos = PdfReader(resource_pdf(2019, 1)).read_infos()

        legenda_ordinario = extract(infos, ColumnHeader.legenda_ordinario)
        legenda_ferie = extract(infos, ColumnHeader.legenda_ferie)
        legenda_reperibilita = extract(infos, ColumnHeader.legenda_reperibilita)
        legenda_rol = extract(infos, ColumnHeader.legenda_rol)

        self.assertEqual(legenda_ordinario, Decimal(70))
        self.assertEqual(legenda_ferie, Decimal(72))
        self.assertEqual(legenda_reperibilita, Decimal('64.5'))
        self.assertEqual(legenda_rol, Decimal(2))

    def test_legenda_2017_02(self) -> None:
        infos = PdfReader(resource_pdf(2017, 2)).read_infos()

        legenda_ordinario = extract(infos, ColumnHeader.legenda_ordinario)
        legenda_straordinario = extract(
            infos, ColumnHeader.legenda_straordinario
        )
        legenda_ferie = extract(infos, ColumnHeader.legenda_ferie)
        legenda_reperibilita = extract(infos, ColumnHeader.legenda_reperibilita)
        legenda_rol = extract(infos, ColumnHeader.legenda_rol)

        self.assertEqual(legenda_ordinario, Decimal(136))
        self.assertEqual(legenda_straordinario, Decimal(2))
        self.assertEqual(legenda_ferie, Decimal(32))
        self.assertEqual(legenda_reperibilita, Decimal(102))
        self.assertEqual(legenda_rol, Decimal(0))

    def test_month_2012_09(self) -> None:
        [info] = PdfReader(resource_pdf(2012, 9)).read_infos()

        self.assertEqual(info.when, date(2012, 9, 1))

    def test_congedo_2024_05(self) -> None:
        infos = PdfReader(resource_pdf(2024, 5)).read_infos()

        self.assertEqual(88, extract(infos, ColumnHeader.legenda_congedo))


def extract(infos: list[Info], key: ColumnHeader) -> Decimal | None:
    for info in infos:
        for column in info.columns:
            if column.header is key:
                return column.howmuch
    raise KeyError
