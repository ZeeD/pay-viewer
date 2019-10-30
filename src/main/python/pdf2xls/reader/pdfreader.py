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
from ..mtime import abcmtimerereader


class PdfReader(abcreader.ABCReader):
    'retrieve infos from .pdf'

    def __init__(self,
                 info_file: typing.BinaryIO,
                mtime_reader: abcmtimerereader.ABCMtimeReader):
        super().__init__(info_file, mtime_reader)
        self.cached_infos: typing.Optional[typing.Iterable[info.Info]] = None

    def read_infos(self) -> typing.Iterable[info.Info]:
        'read from a file'

        if self.cached_infos:
            return self.cached_infos

        tables = tabula.read_pdf(typing.cast(typing.BinaryIO, self.info_file),
                                 multiple_tables=True,
                                 java_options=['-Dsun.java2d.cmm=sun.java2d.cmm.kcms.KcmsServiceProvider'],
                                 guess=False, lattice=True)

        table_periodo = tables[1]
        table_money = tables[5]
        # table_meta = tables[2]
        table_netto_da_pagare = tables[9]
        table_ferie = tables[10]

        when = extract_periodo(table_periodo)

        minimo = extract_minimo(table_money)
        scatti = extract_scatti(table_money)
        superm = extract_superm(table_money)
        sup_ass = extract_sup_ass(table_money)
        edr = extract_edr(table_money)
        totale_retributivo = extract_totale_retributivo(table_money)

        netto_da_pagare = extract_netto_da_pagare(table_netto_da_pagare)

        ferie_a_prec = extract_ferie_a_prec(table_ferie)
        ferie_spett = extract_ferie_spett(table_ferie)
        ferie_godute = extract_ferie_godute(table_ferie)
        ferie_saldo = extract_ferie_saldo(table_ferie)
        par_a_prec = extract_par_a_prec(table_ferie)
        par_spett = extract_par_spett(table_ferie)
        par_godute = extract_par_godute(table_ferie)
        par_saldo = extract_par_saldo(table_ferie)

        self.cached_infos = [
            info.Info(when, minimo, keys.Keys.minimo),
            info.Info(when, scatti, keys.Keys.scatti),
            info.Info(when, superm, keys.Keys.superm),
            info.Info(when, sup_ass, keys.Keys.sup_ass),
            info.Info(when, edr, keys.Keys.edr),
            info.Info(when, totale_retributivo, keys.Keys.totale_retributivo),
            info.Info(when, netto_da_pagare, keys.Keys.netto_da_pagare),
            info.Info(when, ferie_a_prec, keys.Keys.ferie_a_prec),
            info.Info(when, ferie_spett, keys.Keys.ferie_spett),
            info.Info(when, ferie_godute, keys.Keys.ferie_godute),
            info.Info(when, ferie_saldo, keys.Keys.ferie_saldo),
            info.Info(when, par_a_prec, keys.Keys.par_a_prec),
            info.Info(when, par_spett, keys.Keys.par_spett),
            info.Info(when, par_godute, keys.Keys.par_godute),
            info.Info(when, par_saldo, keys.Keys.par_saldo)
        ]
        return self.cached_infos


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
    s: typing.Union[str, float]
    if isinstance(el, float):
        if math.isnan(el):
            s = '0'
        else:
            s = round(el, 2)
    else:
        s = el.replace('.', '').replace(',', '.')
        if s.endswith('-'):
            s = s[-1] + s[:-1]

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


def extract_netto_da_pagare(table: pandas.DataFrame) -> decimal.Decimal:
    return extract(table[0][0].split()[0])


def extract_ferie_a_prec(table: pandas.DataFrame) -> decimal.Decimal:
    return extract(table[1][1])


def extract_ferie_spett(table: pandas.DataFrame) -> decimal.Decimal:
    return extract(table[2][1])


def extract_ferie_godute(table: pandas.DataFrame) -> decimal.Decimal:
    return extract(table[3][1])


def extract_ferie_saldo(table: pandas.DataFrame) -> decimal.Decimal:
    return extract(table[4][1])


def extract_par_a_prec(table: pandas.DataFrame) -> decimal.Decimal:
    return extract(table[1][2])


def extract_par_spett(table: pandas.DataFrame) -> decimal.Decimal:
    return extract(table[2][2])


def extract_par_godute(table: pandas.DataFrame) -> decimal.Decimal:
    return extract(table[3][2])


def extract_par_saldo(table: pandas.DataFrame) -> decimal.Decimal:
    return extract(table[4][2])

