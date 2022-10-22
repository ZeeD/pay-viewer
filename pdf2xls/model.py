from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import auto
from enum import Enum
from typing import Optional


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
    detail = auto()


@dataclass(frozen=True)
class Column:
    header: ColumnHeader
    howmuch: Optional[Decimal]


@dataclass(frozen=True)
class AdditionalDetail:
    prev: Optional[int]
    fisc: Optional[int]
    cod: int
    descrizione: str
    ore_o_giorni: Decimal
    compenso_unitario: Decimal
    trattenute: Decimal
    competenze: Decimal


@dataclass(frozen=True)
class Info:
    when: date
    columns: list[Column]
    additional_details: list[AdditionalDetail]


def parse_infos(infos: list[Info]) -> tuple[list[str], list[list[str]]]:
    headers: list[str] = ['when']
    data: list[list[str]] = []

    indexes: dict[str, int] = {}

    for info in infos:
        row = ['0'] * len(headers)

        # when
        row[0] = str(info.when)

        # columns
        for columns in info.columns:
            key = columns.header.name
            value = str(columns.howmuch)
            if key in indexes:
                row[indexes[key]] = value
            else:
                indexes[key] = len(headers)
                headers.append(key)
                for other_row in data:
                    other_row.append('0')
                row.append(value)

        # additional_details
        for additional_detail in info.additional_details:
            key = str(additional_detail.cod)
            value = str(-additional_detail.trattenute if additional_detail.trattenute else additional_detail.competenze)
            if key in indexes:
                row[indexes[key]] = value
            else:
                indexes[key] = len(headers)
                headers.append(additional_detail.descrizione)  # first one
                for other_row in data:
                    other_row.append('0')
                row.append(value)

        data.append(row)

    return headers, data
