from collections.abc import Iterator
from datetime import date
from decimal import Decimal
from math import isnan
from typing import Any

from pandas import DataFrame
from pandas import options
from tabula.io import read_pdf_with_template

from constants import TEMPLATE_PATH
from model import AdditionalDetail
from model import Column
from model import ColumnHeader
from model import Info

from .abcreader import ABCReader


class PdfReader(ABCReader):
    def read_infos(self) -> list[Info]:
        "Read from a file."
        for name in dir(options.display):
            if 'max' in name:
                setattr(options.display, name, 1000)

        tables = read_pdf_with_template(
            self.name,
            TEMPLATE_PATH,
            pandas_options={'header': None},
            pages=1,
            stream=True,
        )

        table_periodo = tables[0]
        table_money = tables[1]
        table_details = tables[2]
        table_netto_pagare = tables[3]
        # table_dati_fiscali = tables[4]
        table_ferie = tables[5]
        try:
            table_legenda_keys = tables[6]
        except IndexError:
            table_legenda_keys = DataFrame()
        try:
            table_legenda_values = tables[7]
        except IndexError:
            table_legenda_values = DataFrame()

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

        legenda_ordinario = extract_legenda(
            table_legenda_keys, table_legenda_values, 'OR'
        )
        legenda_straordinario = extract_legenda(
            table_legenda_keys, table_legenda_values, 'ST'
        )
        legenda_ferie = extract_legenda(
            table_legenda_keys, table_legenda_values, 'FR'
        )
        legenda_reperibilita = extract_legenda(
            table_legenda_keys, table_legenda_values, 'RA'
        )
        legenda_rol = extract_legenda(
            table_legenda_keys, table_legenda_values, 'RL'
        )

        additional_details = extract_details(table_details)

        info = Info(
            when=when,
            columns=[
                Column(ColumnHeader.minimo, minimo),
                Column(ColumnHeader.scatti, scatti),
                Column(ColumnHeader.superm, superm),
                Column(ColumnHeader.sup_ass, sup_ass),
                Column(ColumnHeader.edr, edr),
                Column(ColumnHeader.totale_retributivo, totale_retributivo),
                Column(ColumnHeader.netto_da_pagare, netto_da_pagare),
                Column(ColumnHeader.ferie_a_prec, ferie_a_prec),
                Column(ColumnHeader.ferie_spett, ferie_spett),
                Column(ColumnHeader.ferie_godute, ferie_godute),
                Column(ColumnHeader.ferie_saldo, ferie_saldo),
                Column(ColumnHeader.par_a_prec, par_a_prec),
                Column(ColumnHeader.par_spett, par_spett),
                Column(ColumnHeader.par_godute, par_godute),
                Column(ColumnHeader.par_saldo, par_saldo),
                Column(ColumnHeader.legenda_ordinario, legenda_ordinario),
                Column(
                    ColumnHeader.legenda_straordinario, legenda_straordinario
                ),
                Column(ColumnHeader.legenda_ferie, legenda_ferie),
                Column(ColumnHeader.legenda_reperibilita, legenda_reperibilita),
                Column(ColumnHeader.legenda_rol, legenda_rol),
            ],
            additional_details=list(additional_details),
        )

        # there is only an info object in a pdf
        return [info]


def extract_periodo(table: DataFrame) -> date:
    "Extract the right row, and parse the date inside."
    cell = table.loc[0, 0]
    assert isinstance(cell, str), type(cell)
    words = cell.split()

    day = 31 if words[0] == '13.MA' else 1
    month = {
        'GENNAIO': 1,
        'FEBBRAIO': 2,
        'MARZO': 3,
        'APRILE': 4,
        'MAGGIO': 5,
        'GIUGNO': 6,
        'LUGLIO': 7,
        'AGOSTO': 8,
        'SETTEMBRE': 9,
        'OTTOBRE': 10,
        'NOVEMBRE': 11,
        'DICEMBRE': 12,
        '13.MA': 12,
    }[words[0]]
    year = int(words[1])

    return date(year, month, day)


def extract(el: str | float) -> Decimal:
    s: str | float
    if isinstance(el, float):
        s = '0' if isnan(el) else round(el, 2)
    else:
        s = el.replace('.', '').replace(',', '.')
        if s.endswith('-'):
            s = s[-1] + s[:-1]

    return Decimal(s)


def extract_minimo(table: DataFrame) -> Decimal:
    el = table.loc[1, 0]
    assert isinstance(el, str | float), type(el)
    return extract(el)


def extract_scatti(table: DataFrame) -> Decimal:
    el = table.loc[1, 1]
    assert isinstance(el, str | float), type(el)
    return extract(el)


def extract_superm(table: DataFrame) -> Decimal:
    el = table.loc[1, 4]
    assert isinstance(el, str | float), type(el)
    return extract(el)


def extract_edr(table: DataFrame) -> Decimal:
    el = table.loc[3, 0]
    assert isinstance(el, str | float), type(el)
    return extract(el)


def extract_sup_ass(table: DataFrame) -> Decimal:
    el = table.loc[1, 5]
    assert isinstance(el, str | float), type(el)
    return extract(el)


def extract_totale_retributivo(table: DataFrame) -> Decimal:
    el = table.loc[3, 8]
    assert isinstance(el, str | float), type(el)
    return extract(el)


def extract_netto_da_pagare(table: DataFrame) -> Decimal:
    try:
        el = table.loc[0, 0]
        assert isinstance(el, str | float), type(el)
        return extract(el)
    except IndexError:
        return Decimal(0)


def extract_ferie_a_prec(table: DataFrame) -> Decimal:
    try:
        el = table.loc[1, 1]
        assert isinstance(el, str | float), type(el)
        return extract(el)
    except IndexError:
        return Decimal(0)


def extract_ferie_spett(table: DataFrame) -> Decimal:
    try:
        el = table.loc[1, 2]
        assert isinstance(el, str | float), type(el)
        return extract(el)
    except IndexError:
        return Decimal(0)


def extract_ferie_godute(table: DataFrame) -> Decimal:
    try:
        el = table.loc[1, 3]
        assert isinstance(el, str | float), type(el)
        return extract(el)
    except IndexError:
        return Decimal(0)


def extract_ferie_saldo(table: DataFrame) -> Decimal:
    try:
        el = table.loc[1, 4]
        assert isinstance(el, str | float), type(el)
        return extract(el)
    except IndexError:
        return Decimal(0)


def extract_par_a_prec(table: DataFrame) -> Decimal:
    try:
        el = table.loc[2, 1]
        assert isinstance(el, str | float), type(el)
        return extract(el)
    except IndexError:
        return Decimal(0)


def extract_par_spett(table: DataFrame) -> Decimal:
    try:
        el = table.loc[2, 2]
        assert isinstance(el, str | float), type(el)
        return extract(el)
    except IndexError:
        return Decimal(0)


def extract_par_godute(table: DataFrame) -> Decimal:
    try:
        el = table.loc[2, 3]
        assert isinstance(el, str | float), type(el)
        return extract(el)
    except IndexError:
        return Decimal(0)


def extract_par_saldo(table: DataFrame) -> Decimal:
    try:
        el = table.loc[2, 4]
        assert isinstance(el, str | float), type(el)
        return extract(el)
    except IndexError:
        return Decimal(0)


def extract_legenda(
    table_keys: DataFrame, table_values: DataFrame, key: str
) -> Decimal:
    for i, row in table_keys.itertuples():
        if row.startswith(f'{key}='):
            return extract(table_values.iloc[i, 0])
    return Decimal(0)


class UnknownRowError(Exception):
    def __init__(self, row: tuple[Any, ...]) -> None:
        super().__init__(row)


def extract_details(table: DataFrame) -> Iterator[AdditionalDetail]:
    for row in table.itertuples(index=False, name=None):
        if len(row) == 8:  # noqa: PLR2004
            yield AdditionalDetail(
                prev=(None if isnan(row[0]) else int(row[0])),
                fisc=(None if isnan(row[1]) else int(row[1])),
                cod=row[2],
                descrizione=row[3],
                ore_o_giorni=extract(row[4]),
                compenso_unitario=extract(row[5]),
                trattenute=extract(row[6]),
                competenze=extract(row[7]),
            )
        elif (
            len(row) == 9 and isnan(row[4]) and all(isnan(e) for e in table[4])  # noqa: PLR2004
        ):
            yield AdditionalDetail(
                prev=(None if isnan(row[0]) else int(row[0])),
                fisc=(None if isnan(row[1]) else int(row[1])),
                cod=row[2],
                descrizione=row[3],
                ore_o_giorni=extract(row[5]),
                compenso_unitario=extract(row[6]),
                trattenute=extract(row[7]),
                competenze=extract(row[8]),
            )
        else:
            raise UnknownRowError(row)
