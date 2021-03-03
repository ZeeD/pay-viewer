'xls writer'

from datetime import date
from decimal import Decimal
from typing import BinaryIO
from typing import Dict
from typing import Iterable
from typing import List
from typing import Tuple
from typing import Union
from typing import cast

from openpyxl.cell import Cell
from openpyxl.utils.cell import get_column_letter
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from ..model.keys import Keys
from .abcwriter import ABCWriter
from .abcwriter import InfoPoints

E = Union[None, str, date, Decimal]

NUMBER_FORMAT_TEXT = '@'
NUMBER_FORMAT_DATE = 'mm-dd-yy'
NUMBER_FORMAT_NUMBER = '0.00'
NUMBER_FORMAT_CURRENCY = r'#,##0.00\ "€"'

VALUE_NUMBER_FORMAT = {
    Keys.periodo: NUMBER_FORMAT_NUMBER,
    Keys.livello_categoria: NUMBER_FORMAT_NUMBER,
    Keys.n_scatti: NUMBER_FORMAT_NUMBER,
    Keys.minimo: NUMBER_FORMAT_CURRENCY,
    Keys.scatti: NUMBER_FORMAT_CURRENCY,
    Keys.superm: NUMBER_FORMAT_CURRENCY,
    Keys.sup_ass: NUMBER_FORMAT_CURRENCY,
    Keys.edr: NUMBER_FORMAT_CURRENCY,
    Keys.totale_retributivo: NUMBER_FORMAT_CURRENCY,
    Keys.ferie_a_prec: NUMBER_FORMAT_NUMBER,
    Keys.ferie_spett: NUMBER_FORMAT_NUMBER,
    Keys.ferie_godute: NUMBER_FORMAT_NUMBER,
    Keys.ferie_saldo: NUMBER_FORMAT_NUMBER,
    Keys.par_a_prec: NUMBER_FORMAT_NUMBER,
    Keys.par_spett: NUMBER_FORMAT_NUMBER,
    Keys.par_godute: NUMBER_FORMAT_NUMBER,
    Keys.par_saldo: NUMBER_FORMAT_NUMBER,
    Keys.netto_da_pagare: NUMBER_FORMAT_CURRENCY,
    Keys.legenda_ordinario: NUMBER_FORMAT_NUMBER,
    Keys.legenda_straordinario: NUMBER_FORMAT_NUMBER,
    Keys.legenda_ferie: NUMBER_FORMAT_NUMBER,
    Keys.legenda_reperibilita: NUMBER_FORMAT_NUMBER,
    Keys.legenda_rol: NUMBER_FORMAT_NUMBER,
    Keys.detail: NUMBER_FORMAT_TEXT
}


class XlsWriter(ABCWriter):
    'write infos on an .xls'

    def __init__(self, info_file: BinaryIO) -> None:
        super().__init__(info_file)

    def write_feature_infos(self, feature: Keys, infos: InfoPoints) -> None:
        'keep track of the stuff to write'

        for info_point in infos:
            self.table[info_point.when][feature.name] = info_point.howmuch

    def close(self) -> None:
        'atomically write all the infos'

        rows = ([self._row('month', NUMBER_FORMAT_TEXT,
                           ((key.name, NUMBER_FORMAT_TEXT) for key in Keys))] +
                [self._row(when, NUMBER_FORMAT_DATE,
                           ((self.table[when].get(key.name, None), VALUE_NUMBER_FORMAT[key])
                            for key in Keys))
                 for when in sorted(self.table)])

        widths: Dict[str, int] = {}
        for row in rows:
            for i, cell in enumerate(row, start=1):
                column_letter = get_column_letter(i)
                widths[column_letter] = max(widths.get(column_letter, 0),
                                            2 * len(str(cell[0])))

        workbook = Workbook(write_only=True)
        try:
            # create the main sheet
            sheet = workbook.create_sheet('main')
            # first set the width of the columns
            for column_letter, width in widths.items():
                sheet.column_dimensions[column_letter].width = width
            # then add the data
            for row in rows:
                sheet.append([self._cell(sheet, *cell) for cell in row])
        finally:
            workbook.save(cast(BinaryIO, self.info_file))

    def _row(self, e: E, fmt: str, it: Iterable[Tuple[E, str]]) -> List[Tuple[E, str]]:
        row = []
        row.append((e, fmt))
        row.extend(it)
        return row

    def _cell(self, sheet: Worksheet, value: E, number_format: str) -> Cell:
        cell = Cell(sheet, value=value)
        cell.number_format = number_format
        return cell
