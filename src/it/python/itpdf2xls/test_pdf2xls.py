from datetime import date
from decimal import Decimal
from unittest import TestCase

from pdf2xls.model import Column
from pdf2xls.model import ColumnHeader
from pdf2xls.model import Info
from pdf2xls.reader.pdfreader import PdfReader

from . import loadResourcePdf


class TestPdf2Xls(TestCase):
    'test pdf2xls functions'

    def testReadRealPdf(self) -> None:
        expected = [
            Info(when=date(2019, 1, 1),
                 columns=[Column(ColumnHeader.minimo, Decimal('2061.41')),
                          Column(ColumnHeader.scatti, Decimal('109.23')),
                          Column(ColumnHeader.superm, Decimal('50.87')),
                          Column(ColumnHeader.sup_ass, Decimal('674.16')),
                          Column(ColumnHeader.edr, Decimal('0')),
                          Column(ColumnHeader.totale_retributivo,
                                 Decimal('2895.67')),
                          Column(ColumnHeader.ferie_a_prec, Decimal('-1.82')),
                          Column(ColumnHeader.ferie_spett, Decimal('1.67')),
                          Column(ColumnHeader.ferie_godute, Decimal('0')),
                          Column(ColumnHeader.ferie_saldo, Decimal('-0.15')),
                          Column(ColumnHeader.par_a_prec, Decimal('594.68')),
                          Column(ColumnHeader.par_spett, Decimal('8.67')),
                          Column(ColumnHeader.par_godute, Decimal('0')),
                          Column(ColumnHeader.par_saldo, Decimal('603.35')),
                          Column(ColumnHeader.netto_da_pagare,
                                 Decimal('2090.00'))
                          ],
                 additional_details=[])
        ]

        actual = PdfReader(loadResourcePdf(2019, 1)).read_infos()
        self.assertListEqual(expected, actual)
