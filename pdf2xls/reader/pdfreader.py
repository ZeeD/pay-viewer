'pdf reader'

import datetime
import decimal
import math
import typing

import pandas
import tabula

from . import abcreader
from ..model import info
from ..model import keys


class PdfReader(abcreader.ABCReader):
    'retrieve infos from .pdf'

    def read_infos(self,
                   info_file: typing.BinaryIO
                   ) -> typing.Iterable[info.Info]:
        'read from a file'

        tables = tabula.read_pdf(info_file, multiple_tables=True,
                                 java_options=['-Dsun.java2d.cmm=sun.java2d.cmm.kcms.KcmsServiceProvider'],
                                 guess=False, lattice=True)

        table_periodo = tables[1]
        table_money = tables[5]
        # table_meta = tables[2]

        when = extract_periodo(table_periodo)

        minimo = extract_minimo(table_money)
        scatti = extract_scatti(table_money)
        superm = extract_superm(table_money)
        sup_ass = extract_sup_ass(table_money)
        edr = extract_edr(table_money)
        totale_retributivo = extract_totale_retributivo(table_money)

        return [
            info.Info(when, minimo, keys.Keys.minimo),
            info.Info(when, scatti, keys.Keys.scatti),
            info.Info(when, superm, keys.Keys.superm),
            info.Info(when, sup_ass, keys.Keys.sup_ass),
            info.Info(when, edr, keys.Keys.edr),
            info.Info(when, totale_retributivo, keys.Keys.totale_retributivo)
        ]


def extract_periodo(table: pandas.DataFrame) -> datetime.date:
    'extract the right row, and parse the date inside'

    cell = table[0][0]
    words = cell.split(':')[1].split()

    day = 31 if words[0] == '13.MA' else 1
    month = {
        'GENNAIO': 1, 'FEBBRAIO': 2, 'MARZO': 3, 'APRILE': 4,
        'MAGGIO': 5, 'GIUGNO': 6, 'LUGLIO': 7, 'AGOSTO': 8,
        'SETTEMBRE': 9, 'OTTOBRE': 10, 'NOVEMBRE': 11, 'DICEMBRE': 12,
        '13.MA': 12
    }[words[0]]
    year = int(words[1])

    return datetime.date(year, month, day)


def extract(el: typing.Union[str, float]) -> decimal.Decimal:
    s: String = None
    if isinstance(el, float):
        if math.isnan(el):
            s = '0'
        else:
            s = round(el, 2)
    else:
        s = el.replace('.', '').replace(',', '.')

    return decimal.Decimal(s)


def extract_minimo(table: pandas.DataFrame) -> decimal.Decimal:
    return extract(table[0][1])


def extract_scatti(table: pandas.DataFrame) -> decimal.Decimal:
    return extract(table[1][1])


def extract_superm(table: pandas.DataFrame) -> decimal.Decimal:
    return extract(table[4][1])


def extract_edr(table: pandas.DataFrame) -> decimal.Decimal:
    return extract(table[0][3])


def extract_sup_ass(table: pandas.DataFrame) -> decimal.Decimal:
    return extract(table[5][1])


def extract_totale_retributivo(table: pandas.DataFrame) -> decimal.Decimal:
    return extract(table[8][3])
