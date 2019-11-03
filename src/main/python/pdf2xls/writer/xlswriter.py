'xls writer'

import datetime
import decimal
import typing

import openpyxl
import openpyxl.cell

from . import abcwriter
from ..model import info
from ..model import keys

NUMBER_FORMAT_TEXT = '@'
NUMBER_FORMAT_DATE = 'mm-dd-yy'
NUMBER_FORMAT_NUMBER = '0.00'
NUMBER_FORMAT_CURRENCY = r'#,##0.00\ "€"'

VALUE_NUMBER_FORMAT = {
    keys.Keys.periodo: NUMBER_FORMAT_NUMBER,
    keys.Keys.livello_categoria: NUMBER_FORMAT_NUMBER,
    keys.Keys.n_scatti: NUMBER_FORMAT_NUMBER,
    keys.Keys.minimo: NUMBER_FORMAT_CURRENCY,
    keys.Keys.scatti: NUMBER_FORMAT_CURRENCY,
    keys.Keys.superm: NUMBER_FORMAT_CURRENCY,
    keys.Keys.sup_ass: NUMBER_FORMAT_CURRENCY,
    keys.Keys.edr: NUMBER_FORMAT_CURRENCY,
    keys.Keys.totale_retributivo: NUMBER_FORMAT_CURRENCY,
    keys.Keys.ferie_a_prec: NUMBER_FORMAT_NUMBER,
    keys.Keys.ferie_spett: NUMBER_FORMAT_NUMBER,
    keys.Keys.ferie_godute: NUMBER_FORMAT_NUMBER,
    keys.Keys.ferie_saldo: NUMBER_FORMAT_NUMBER,
    keys.Keys.par_a_prec: NUMBER_FORMAT_NUMBER,
    keys.Keys.par_spett: NUMBER_FORMAT_NUMBER,
    keys.Keys.par_godute: NUMBER_FORMAT_NUMBER,
    keys.Keys.par_saldo: NUMBER_FORMAT_NUMBER,
    keys.Keys.netto_da_pagare: NUMBER_FORMAT_CURRENCY
}


class XlsWriter(abcwriter.ABCWriter):
    'write infos on an .xls'

    def __init__(self, info_file: typing.BinaryIO) -> None:
        super().__init__(info_file)
        self.workbook = openpyxl.Workbook(write_only=True)
        self.sheet = self.workbook.create_sheet('main')
        self.sheet.append([self._cell('month', NUMBER_FORMAT_TEXT)] + 
                          [self._cell(key.name, NUMBER_FORMAT_TEXT)
                           for key in keys.Keys])

    def write_feature_infos(self,
                            feature: keys.Keys,
                            infos: typing.Iterable[info.InfoPoint]) -> None:
        'keep track of the stuff to write'

        for info_point in infos:
            self.table[info_point.when][feature.name] = info_point.howmuch

    def close(self) -> None:
        'atomically write all the infos'

        for when in sorted(self.table):
            features: typing.Dict[str, decimal.Decimal] = self.table[when]
            self.sheet.append([self._cell(when, NUMBER_FORMAT_DATE)] + 
                              [self._cell(features.get(key.name, None),
                                          VALUE_NUMBER_FORMAT[key])
                               for key in keys.Keys])

        self.workbook.save(typing.cast(typing.BinaryIO, self.info_file))

    def _cell(self,
              value: typing.Union[None, str, datetime.date, decimal.Decimal],
              number_format: str
              ) -> openpyxl.cell.Cell:
        cell = openpyxl.cell.Cell(self.sheet, value=value)
        cell.number_format = number_format  # pylint: disable=assigning-non-slot
        return cell
