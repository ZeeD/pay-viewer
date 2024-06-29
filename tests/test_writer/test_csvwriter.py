from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Final
from unittest import TestCase
from unittest.mock import call
from unittest.mock import mock_open
from unittest.mock import patch

from payviewer.model import AdditionalDetail
from payviewer.model import Column
from payviewer.model import ColumnHeader
from payviewer.model import Info
from payviewer.writer.csvwriter import CsvWriter
from payviewer.writer.csvwriter import fieldnames
from payviewer.writer.csvwriter import rows

INFOS: Final = [
    Info(
        date(1982, 5, 11),
        [Column(ColumnHeader.minimo, Decimal(1))],
        [
            AdditionalDetail(
                None,
                None,
                0,
                'descrizione 1',
                Decimal(0),
                Decimal(0),
                Decimal(2),
                Decimal(3),
            )
        ],
    ),
    Info(
        date(1989, 7, 27),
        [Column(ColumnHeader.legenda_ferie, Decimal(4))],
        [
            AdditionalDetail(
                None,
                None,
                0,
                'descrizione 2',
                Decimal(0),
                Decimal(0),
                Decimal(50),
                Decimal(60),
            )
        ],
    ),
]


class TestCsvWriter(TestCase):
    def test_fieldnames(self) -> None:
        expected = [
            'month',
            'periodo',
            'livello_categoria',
            'n_scatti',
            'minimo',
            'scatti',
            'superm',
            'sup_ass',
            'edr',
            'totale_retributivo',
            'ferie_a_prec',
            'ferie_spett',
            'ferie_godute',
            'ferie_saldo',
            'par_a_prec',
            'par_spett',
            'par_godute',
            'par_saldo',
            'netto_da_pagare',
            'legenda_ordinario',
            'legenda_straordinario',
            'legenda_ferie',
            'legenda_reperibilita',
            'legenda_rol',
            'legenda_congedo',
            'descrizione 1',
            'descrizione 2',
        ]
        actual = fieldnames(INFOS)
        self.assertListEqual(expected, actual)

    def test_rows(self) -> None:
        expected = [
            {
                'month': date(1982, 5, 11),
                'minimo': Decimal('1'),
                'descrizione 1': Decimal('1'),
            },
            {
                'month': date(1989, 7, 27),
                'legenda_ferie': Decimal('4'),
                'descrizione 2': Decimal('10'),
            },
        ]
        actual = rows(INFOS)
        self.assertListEqual(expected, actual)

    def test_write_infos(self) -> None:
        expected = [
            'month,periodo,livello_categoria,n_scatti,minimo,scatti,superm,sup_ass,edr,totale_retributivo,ferie_a_prec,ferie_spett,ferie_godute,ferie_saldo,par_a_prec,par_spett,par_godute,par_saldo,netto_da_pagare,legenda_ordinario,legenda_straordinario,legenda_ferie,legenda_reperibilita,legenda_rol,legenda_congedo,descrizione 1,descrizione 2\r\n',  # noqa: E501
            '1982-05-11,,,,1,,,,,,,,,,,,,,,,,,,,,1,\r\n',
            '1989-07-27,,,,,,,,,,,,,,,,,,,,,4,,,,,10\r\n',
        ]

        mock = mock_open()
        with patch('pathlib.io.open', mock):
            CsvWriter(Path()).write_infos(INFOS)

        mock().write.assert_has_calls([call(e) for e in expected])
