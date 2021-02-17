'pdf reader'

import datetime
import decimal
import math
import typing

import pandas
import tabula

from ..model import info
from ..model import keys
from ..mtime import abcmtimerereader
from . import abcreader

TEMPLATE_PATH = f'{__file__}/../../../../resources/tabula-template.json'


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

#         [setattr(pandas.options.display, name, 1000)
#          for name in dir(pandas.options.display) if 'max' in name]

        tables = tabula.read_pdf_with_template(typing.cast(typing.BinaryIO, self.info_file),
                                               TEMPLATE_PATH,
                                               pandas_options={'header': None},
                                               pages=1,
                                               stream=True)

        table_periodo = tables[0]
        table_money = tables[1]
        table_details = tables[2]
        table_netto_pagare = tables[3]
        table_dati_fiscali = tables[4]
        table_ferie = tables[5]
        try:
            table_legenda_keys = tables[6]
        except IndexError:
            table_legenda_keys = pandas.DataFrame()
        try:
            table_legenda_values = tables[7]
        except IndexError:
            table_legenda_values = pandas.DataFrame()

        when = extract_periodo(table_periodo)

        minimo = extract_minimo(table_money)
        scatti = extract_scatti(table_money)
        superm = extract_superm(table_money)
        sup_ass = extract_sup_ass(table_money)
        edr = extract_edr(table_money)
        totale_retributivo = extract_totale_retributivo(table_money)

        netto_da_pagare = extract_netto_da_pagare(table_netto_pagare)

        ferie_a_prec = extract_ferie_a_prec(table_ferie)
        ferie_spett = extract_ferie_spett(table_ferie)
        ferie_godute = extract_ferie_godute(table_ferie)
        ferie_saldo = extract_ferie_saldo(table_ferie)
        par_a_prec = extract_par_a_prec(table_ferie)
        par_spett = extract_par_spett(table_ferie)
        par_godute = extract_par_godute(table_ferie)
        par_saldo = extract_par_saldo(table_ferie)

        legenda_ordinario = extract_legenda(table_legenda_keys,
                                            table_legenda_values,
                                            'OR')
        legenda_straordinario = extract_legenda(table_legenda_keys,
                                                table_legenda_values,
                                                'ST')
        legenda_ferie = extract_legenda(table_legenda_keys,
                                        table_legenda_values,
                                        'FR')
        legenda_reperibilita = extract_legenda(table_legenda_keys,
                                               table_legenda_values,
                                               'RA')
        legenda_rol = extract_legenda(table_legenda_keys,
                                      table_legenda_values,
                                      'RL')

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
            info.Info(when, par_saldo, keys.Keys.par_saldo),
            info.Info(when, legenda_ordinario, keys.Keys.legenda_ordinario),
            info.Info(when, legenda_straordinario,
                      keys.Keys.legenda_straordinario),
            info.Info(when, legenda_ferie, keys.Keys.legenda_ferie),
            info.Info(when, legenda_reperibilita,
                      keys.Keys.legenda_reperibilita),
            info.Info(when, legenda_rol, keys.Keys.legenda_rol)
        ]
        return self.cached_infos


def extract_periodo(table: pandas.DataFrame) -> datetime.date:
    'extract the right row, and parse the date inside'

    cell = typing.cast(str, table.at[0, 0])
    words = cell.split()

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
    return extract(table.at[1, 0])


def extract_scatti(table: pandas.DataFrame) -> decimal.Decimal:
    return extract(table.at[1, 1])


def extract_superm(table: pandas.DataFrame) -> decimal.Decimal:
    return extract(table.at[1, 4])


def extract_edr(table: pandas.DataFrame) -> decimal.Decimal:
    return extract(table.at[3, 0])


def extract_sup_ass(table: pandas.DataFrame) -> decimal.Decimal:
    return extract(table.at[1, 5])


def extract_totale_retributivo(table: pandas.DataFrame) -> decimal.Decimal:
    return extract(table.at[3, 8])


def extract_netto_da_pagare(table: pandas.DataFrame) -> decimal.Decimal:
    try:
        return extract(typing.cast(str, table.at[0, 0]))
    except IndexError:
        return decimal.Decimal(0)


def extract_ferie_a_prec(table: pandas.DataFrame) -> decimal.Decimal:
    try:
        return extract(typing.cast(str, table.at[1, 1]))
    except IndexError:
        return decimal.Decimal(0)


def extract_ferie_spett(table: pandas.DataFrame) -> decimal.Decimal:
    try:
        return extract(typing.cast(str, table.at[1, 2]))
    except IndexError:
        return decimal.Decimal(0)


def extract_ferie_godute(table: pandas.DataFrame) -> decimal.Decimal:
    try:
        return extract(typing.cast(str, table.at[1, 3]))
    except IndexError:
        return decimal.Decimal(0)


def extract_ferie_saldo(table: pandas.DataFrame) -> decimal.Decimal:
    try:
        return extract(typing.cast(str, table.at[1, 4]))
    except IndexError:
        return decimal.Decimal(0)


def extract_par_a_prec(table: pandas.DataFrame) -> decimal.Decimal:
    try:
        return extract(typing.cast(str, table.at[2, 1]))
    except IndexError:
        return decimal.Decimal(0)


def extract_par_spett(table: pandas.DataFrame) -> decimal.Decimal:
    try:
        return extract(typing.cast(str, table.at[2, 2]))
    except IndexError:
        return decimal.Decimal(0)


def extract_par_godute(table: pandas.DataFrame) -> decimal.Decimal:
    try:
        return extract(typing.cast(str, table.at[2, 3]))
    except IndexError:
        return decimal.Decimal(0)


def extract_par_saldo(table: pandas.DataFrame) -> decimal.Decimal:
    try:
        return extract(typing.cast(str, table.at[2, 4]))
    except IndexError:
        return decimal.Decimal(0)


def extract_legenda(table_keys: pandas.DataFrame,
                    table_values: pandas.DataFrame,
                    key: str
                    ) -> decimal.Decimal:
    for i, row in table_keys.itertuples():
        if row.startswith(f'{key}='):
            return extract(table_values.iloc[i, 0])
    return decimal.Decimal(0)
