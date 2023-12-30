from datetime import date
from decimal import Decimal
from unittest import TestCase

from payviewer.model import AdditionalDetail
from payviewer.model import Column
from payviewer.model import ColumnHeader
from payviewer.model import Info
from payviewer.reader.pdfreader import PdfReader
from testsupport import resource_pdf

ZERO = Decimal('0')


class TestPdf2Xls(TestCase):

    "test pdf2xls functions."

    def test_read_real_pdf(self) -> None:
        expected = [
            Info(
                date(2019, 1, 1),
                [
                    Column(ColumnHeader.minimo, Decimal('2061.41')),
                    Column(ColumnHeader.scatti, Decimal('109.23')),
                    Column(ColumnHeader.superm, Decimal('50.87')),
                    Column(ColumnHeader.sup_ass, Decimal('674.16')),
                    Column(ColumnHeader.edr, ZERO),
                    Column(ColumnHeader.totale_retributivo, Decimal('2895.67')),
                    Column(ColumnHeader.netto_da_pagare, Decimal('2090')),
                    Column(ColumnHeader.ferie_a_prec, Decimal('-1.82')),
                    Column(ColumnHeader.ferie_spett, Decimal('1.67')),
                    Column(ColumnHeader.ferie_godute, ZERO),
                    Column(ColumnHeader.ferie_saldo, Decimal('-0.15')),
                    Column(ColumnHeader.par_a_prec, Decimal('594.68')),
                    Column(ColumnHeader.par_spett, Decimal('8.67')),
                    Column(ColumnHeader.par_godute, ZERO),
                    Column(ColumnHeader.par_saldo, Decimal('603.35')),
                    Column(ColumnHeader.legenda_ordinario, Decimal('70')),
                    Column(ColumnHeader.legenda_straordinario, ZERO),
                    Column(ColumnHeader.legenda_ferie, Decimal('72')),
                    Column(ColumnHeader.legenda_reperibilita, Decimal('64.5')),
                    Column(ColumnHeader.legenda_rol, Decimal('2')),
                ],
                [
                    AdditionalDetail(
                        1,
                        1,
                        2000,
                        'STIPENDIO',
                        Decimal('26'),
                        Decimal('111.37192'),
                        ZERO,
                        Decimal('2895.67'),
                    ),
                    AdditionalDetail(
                        0,
                        0,
                        2308,
                        'TICKET PASTO E109,20',
                        Decimal('21'),
                        Decimal('5.2'),
                        ZERO,
                        ZERO,
                    ),
                    AdditionalDetail(
                        1,
                        1,
                        2803,
                        'INDENN.REPERIB.FORF.',
                        ZERO,
                        ZERO,
                        ZERO,
                        Decimal('61.25'),
                    ),
                    AdditionalDetail(
                        1,
                        1,
                        2804,
                        'INDENN.REPERIB.FESTIVO',
                        ZERO,
                        ZERO,
                        ZERO,
                        Decimal('258.50'),
                    ),
                    AdditionalDetail(
                        0,
                        0,
                        4802,
                        'FERIE GODUTE',
                        Decimal('9'),
                        ZERO,
                        ZERO,
                        ZERO,
                    ),
                    AdditionalDetail(
                        0, 0, 4806, 'PAR GODUTE', Decimal('2'), ZERO, ZERO, ZERO
                    ),
                    AdditionalDetail(
                        None,
                        None,
                        5550,
                        'IMPONIBILE NON ARROTOND.',
                        ZERO,
                        Decimal('3215.42'),
                        ZERO,
                        ZERO,
                    ),
                    AdditionalDetail(
                        0,
                        0,
                        5792,
                        'F.METASALUTE C/AZ.',
                        ZERO,
                        Decimal('13'),
                        ZERO,
                        ZERO,
                    ),
                    AdditionalDetail(
                        None,
                        2,
                        5817,
                        'CONTRIBUTO F.A.P. 9,19%',
                        Decimal('9.19'),
                        Decimal('3215'),
                        Decimal('295.46'),
                        ZERO,
                    ),
                    AdditionalDetail(
                        None,
                        2,
                        5860,
                        'CONTRIBUTO F.A.P. 0,30%',
                        Decimal('.3'),
                        Decimal('3215'),
                        Decimal('9.65'),
                        ZERO,
                    ),
                    AdditionalDetail(
                        None,
                        None,
                        6841,
                        'ADDIZ. REGIONALE A.P.',
                        ZERO,
                        ZERO,
                        Decimal('53.52'),
                        ZERO,
                    ),
                    AdditionalDetail(
                        None,
                        None,
                        6842,
                        'IMPOSTA NETTA (COD.1001)',
                        ZERO,
                        ZERO,
                        Decimal('746.45'),
                        ZERO,
                    ),
                    AdditionalDetail(
                        None,
                        None,
                        6851,
                        'ADDIZ. COMUNALE A.P.',
                        ZERO,
                        ZERO,
                        Decimal('20.94'),
                        ZERO,
                    ),
                    AdditionalDetail(
                        0,
                        0,
                        6857,
                        'AD.COM.LE RESIDUA A.P.',
                        ZERO,
                        Decimal('209.39'),
                        ZERO,
                        ZERO,
                    ),
                    AdditionalDetail(
                        0,
                        0,
                        6858,
                        'AD.REG.LE RESIDUA A.P.',
                        ZERO,
                        Decimal('535.21'),
                        ZERO,
                        ZERO,
                    ),
                    AdditionalDetail(
                        0,
                        0,
                        6866,
                        'AD.LE COM.LE 30% TOTALE',
                        ZERO,
                        Decimal('95.74'),
                        ZERO,
                        ZERO,
                    ),
                    AdditionalDetail(
                        None,
                        None,
                        6985,
                        'ARR.MESE PRECED.',
                        ZERO,
                        ZERO,
                        Decimal('.14'),
                        ZERO,
                    ),
                    AdditionalDetail(
                        None,
                        None,
                        6989,
                        'ARROTONDAMENTO',
                        ZERO,
                        ZERO,
                        ZERO,
                        Decimal('.74'),
                    ),
                ],
            )
        ]

        actual = PdfReader(resource_pdf(2019, 1)).read_infos()
        self.assertEqual(len(expected), len(actual))
        self.assertEqual(expected[0].when, actual[0].when)
        self.assertListEqual(expected[0].columns, actual[0].columns)
        self.assertListEqual(
            expected[0].additional_details, actual[0].additional_details
        )
