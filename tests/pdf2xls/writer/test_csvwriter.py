from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Final
from unittest import TestCase
from unittest.mock import call
from unittest.mock import mock_open
from unittest.mock import patch

from pdf2xls.model import AdditionalDetail
from pdf2xls.model import Column
from pdf2xls.model import ColumnHeader
from pdf2xls.model import Info
from pdf2xls.writer.csvwriter import CsvWriter
from pdf2xls.writer.csvwriter import fieldnames
from pdf2xls.writer.csvwriter import rows

INFOS: Final = [Info(date(1982, 5, 11),
                     [Column(ColumnHeader.minimo, Decimal(1))],
                     [AdditionalDetail(None, None, 0,
                                       'descrizione 1',
                                       Decimal(0), Decimal(0),
                                       Decimal(2), Decimal(3))]),
                Info(date(1989, 7, 27),
                     [Column(ColumnHeader.legenda_ferie, Decimal(4))],
                     [AdditionalDetail(None, None, 0,
                                       'descrizione 2',
                                       Decimal(0), Decimal(0),
                                       Decimal(50), Decimal(60))])]


class TestCsvWriter(TestCase):
    def test_fieldnames(self) -> None:
        expected = ['month',
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
                    'descrizione 1',
                    'descrizione 2']
        actual = fieldnames(INFOS)
        self.assertListEqual(expected, actual)

    def test_rows(self) -> None:
        expected = [{'month': date(1982, 5, 11),
                     'minimo': Decimal('1'),
                     'descrizione 1': Decimal('1')},
                    {'month': date(1989, 7, 27),
                     'legenda_ferie': Decimal('4'),
                     'descrizione 2': Decimal('10')}]
        actual = rows(INFOS)
        self.assertListEqual(expected, actual)

    def test_write_infos(self) -> None:
        expected = [
            'month,periodo,livello_categoria,n_scatti,minimo,scatti,superm,sup_ass,edr,totale_retributivo,ferie_a_prec,ferie_spett,ferie_godute,ferie_saldo,par_a_prec,par_spett,par_godute,par_saldo,netto_da_pagare,legenda_ordinario,legenda_straordinario,legenda_ferie,legenda_reperibilita,legenda_rol,descrizione 1,descrizione 2\r\n',
            '1982-05-11,,,,1,,,,,,,,,,,,,,,,,,,,1,\r\n',
            '1989-07-27,,,,,,,,,,,,,,,,,,,,,4,,,,10\r\n'
        ]

        mock = mock_open()
        with patch('pdf2xls.writer.csvwriter.open', mock):
            CsvWriter(Path()).write_infos(INFOS)

        mock().write.assert_has_calls([call(e) for e in expected])
