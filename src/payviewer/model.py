from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum
from enum import auto
from operator import attrgetter
from pathlib import Path

ZERO = Decimal(0)


class ColumnHeader(Enum):
    periodo = auto()
    livello_categoria = auto()
    n_scatti = auto()
    minimo = auto()
    scatti = auto()
    superm = auto()
    sup_ass = auto()
    edr = auto()
    totale_retributivo = auto()
    ferie_a_prec = auto()
    ferie_spett = auto()
    ferie_godute = auto()
    ferie_saldo = auto()
    par_a_prec = auto()
    par_spett = auto()
    par_godute = auto()
    par_saldo = auto()
    netto_da_pagare = auto()
    legenda_ordinario = auto()
    legenda_straordinario = auto()
    legenda_ferie = auto()
    legenda_reperibilita = auto()
    legenda_rol = auto()
    legenda_congedo = auto()
    detail = auto()
    ticket_pasto = auto()


@dataclass(frozen=True)
class Column:
    header: ColumnHeader
    howmuch: 'Decimal | None'


@dataclass(frozen=True)
class AdditionalDetail:
    prev: int | None
    fisc: int | None
    cod: int
    descrizione: str
    ore_o_giorni: 'Decimal'
    compenso_unitario: 'Decimal'
    trattenute: 'Decimal'
    competenze: 'Decimal'


@dataclass(frozen=True)
class Info:
    when: 'date'
    columns: list[Column]
    additional_details: list[AdditionalDetail]
    path: 'Path'

    def howmuch(self, header: ColumnHeader) -> 'Decimal | None':
        for column in self.columns:
            if column.header == header:
                return column.howmuch
        return None


def get_descrizione(additional_detail: AdditionalDetail) -> str:
    return {
        2302: 'TICKET PASTO C',
        2308: 'TICKET PASTO E',
        2802: 'REPER. INTERVENTO',
        6854: 'AD.COM.LE DA TR.',
        6856: 'AD.REG.LE DA TR.',
        7293: 'ULT.DETRAZIONE MESE/PROGR',
    }.get(additional_detail.cod, additional_detail.descrizione)


def parse_infos(
    infos: list[Info],
) -> 'tuple[list[str], list[tuple[Path, date]], list[list[Decimal]]]':
    headers: list[str] = ['when']
    whens: list[tuple[Path, date]] = []
    data: list[list[Decimal]] = []

    indexes: dict[str, int] = {}

    for info in sorted(infos, key=attrgetter('when'), reverse=True):
        row = [ZERO] * (len(headers) - 1)

        # preview+when
        whens.append((info.path, info.when))

        # columns
        for columns in sorted(
            info.columns, key=lambda column: column.header.name
        ):
            key = columns.header.name
            value = ZERO if columns.howmuch is None else columns.howmuch
            if key in indexes:
                row[indexes[key]] = value
            else:
                indexes[key] = len(headers) - 1
                headers.append(key)
                for other_row in data:
                    other_row.append(ZERO)
                row.append(value)

        # additional_details
        for additional_detail in sorted(
            info.additional_details, key=attrgetter('descrizione')
        ):
            key = str(additional_detail.cod)
            value = (
                -additional_detail.trattenute
                if additional_detail.trattenute
                else additional_detail.competenze
            )
            if key in indexes:
                row[indexes[key]] = value
            else:
                indexes[key] = len(headers) - 1
                headers.append(get_descrizione(additional_detail))  # first one
                for other_row in data:
                    other_row.append(ZERO)
                row.append(value)

        data.append(row)

    return headers, whens, data
