from datetime import date
from decimal import Decimal
from unittest import TestCase

from pdf2xls.model import AdditionalDetail
from pdf2xls.model import Column
from pdf2xls.model import ColumnHeader
from pdf2xls.model import Info
from pdf2xls.reader.pdfreader import PdfReader

from . import loadResourcePdf


class TestPdf2Xls(TestCase):
    'test pdf2xls functions'

    def testReadRealPdf(self) -> None:
        expected = [
            Info(date(2019, 1, 1),
                 [Column(ColumnHeader.minimo, Decimal('2061.41')),
                  Column(ColumnHeader.scatti, Decimal('109.23')),
                  Column(ColumnHeader.superm, Decimal('50.87')),
                  Column(ColumnHeader.sup_ass, Decimal('674.16')),
                  Column(ColumnHeader.edr, Decimal('0')),
                  Column(ColumnHeader.totale_retributivo, Decimal('2895.67')),
                  Column(ColumnHeader.netto_da_pagare, Decimal('2090')),
                  Column(ColumnHeader.ferie_a_prec, Decimal('-1.82')),
                  Column(ColumnHeader.ferie_spett, Decimal('1.67')),
                  Column(ColumnHeader.ferie_godute, Decimal('0')),
                  Column(ColumnHeader.ferie_saldo, Decimal('-0.15')),
                  Column(ColumnHeader.par_a_prec, Decimal('594.68')),
                  Column(ColumnHeader.par_spett, Decimal('8.67')),
                  Column(ColumnHeader.par_godute, Decimal('0')),
                  Column(ColumnHeader.par_saldo, Decimal('603.35')),
                  Column(ColumnHeader.legenda_ordinario, Decimal('70')),
                  Column(ColumnHeader.legenda_straordinario, Decimal('0')),
                  Column(ColumnHeader.legenda_ferie, Decimal('72')),
                  Column(ColumnHeader.legenda_reperibilita, Decimal('64.5')),
                  Column(ColumnHeader.legenda_rol, Decimal('2'))],
                 [AdditionalDetail(1, 1, 2000, 'STIPENDIO',
                                   Decimal('26'), Decimal('111.37192'), Decimal('0'), Decimal('2895.67')),
                  AdditionalDetail(0, 0, 2308, 'TICKET PASTO E109,20',
                                   Decimal('21'), Decimal('5.2'), Decimal('0'), Decimal('0')),
                  AdditionalDetail(1, 1, 2803, 'INDENN.REPERIB.FORF.',
                                   Decimal('0'), Decimal('0'), Decimal('0'), Decimal('61.25')),
                  AdditionalDetail(1, 1, 2804, 'INDENN.REPERIB.FESTIVO',
                                   Decimal('0'), Decimal('0'), Decimal('0'), Decimal('258.50')),
                  AdditionalDetail(0, 0, 4802, 'FERIE GODUTE',
                                   Decimal('9'), Decimal('0'), Decimal('0'), Decimal('0')),
                  AdditionalDetail(0, 0, 4806, 'PAR GODUTE',
                                   Decimal('2'), Decimal('0'), Decimal('0'), Decimal('0')),
                  AdditionalDetail(None, None, 5550, 'IMPONIBILE NON ARROTOND.',
                                   Decimal('0'), Decimal('3215.42'), Decimal('0'), Decimal('0')),
                  AdditionalDetail(0, 0, 5792, 'F.METASALUTE C/AZ.',
                                   Decimal('0'), Decimal('13'), Decimal('0'), Decimal('0')),
                  AdditionalDetail(None, 2, 5817, 'CONTRIBUTO F.A.P. 9,19%',
                                   Decimal('9.19'), Decimal('3215'), Decimal('295.46'), Decimal('0')),
                  AdditionalDetail(None, 2, 5860, 'CONTRIBUTO F.A.P. 0,30%',
                                   Decimal('.3'), Decimal('3215'), Decimal('9.65'), Decimal('0')),
                  AdditionalDetail(None, None, 6841, 'ADDIZ. REGIONALE A.P.',
                                   Decimal('0'), Decimal('0'), Decimal('53.52'), Decimal('0')),
                  AdditionalDetail(None, None, 6842, 'IMPOSTA NETTA (COD.1001)',
                                   Decimal('0'), Decimal('0'), Decimal('746.45'), Decimal('0')),
                  AdditionalDetail(None, None, 6851, 'ADDIZ. COMUNALE A.P.',
                                   Decimal('0'), Decimal('0'), Decimal('20.94'), Decimal('0')),
                  AdditionalDetail(0, 0, 6857, 'AD.COM.LE RESIDUA A.P.',
                                   Decimal('0'), Decimal('209.39'), Decimal('0'), Decimal('0')),
                  AdditionalDetail(0, 0, 6858, 'AD.REG.LE RESIDUA A.P.',
                                   Decimal('0'), Decimal('535.21'), Decimal('0'), Decimal('0')),
                  AdditionalDetail(0, 0, 6866, 'AD.LE COM.LE 30% TOTALE',
                                   Decimal('0'), Decimal('95.74'), Decimal('0'), Decimal('0')),
                  AdditionalDetail(None, None, 6985, 'ARR.MESE PRECED.',
                                   Decimal('0'), Decimal('0'), Decimal('.14'), Decimal('0')),
                  AdditionalDetail(None, None, 6989, 'ARROTONDAMENTO',
                                   Decimal('0'), Decimal('0'), Decimal('0'), Decimal('.74'))])
        ]

        actual = PdfReader(loadResourcePdf(2019, 1)).read_infos()
        self.assertEqual(len(expected), len(actual))
        self.assertEqual(expected[0].when, actual[0].when)
        self.assertListEqual(expected[0].columns, actual[0].columns)
        self.assertListEqual(expected[0].additional_details,
                             actual[0].additional_details)
