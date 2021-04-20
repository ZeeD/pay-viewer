from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum
from enum import auto
from typing import List
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
    columns: List[Column]
    additional_details: List[AdditionalDetail]
