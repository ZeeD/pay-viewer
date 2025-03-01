#!/usr/bin/env python

from json import load
from logging import INFO
from logging import basicConfig
from logging import info
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator


def all_ticketcods() -> 'Iterator[int]':
    for filename in sorted(
        Path(__file__).parent.glob('../../pay-data/**/*.pdf.json')
    ):
        with filename.open(encoding='utf-8') as fp:
            for obj in load(fp):
                for additional_detail in obj['additional_details']:
                    cod = additional_detail['cod']
                    if not isinstance(cod, int):
                        raise TypeError(cod)
                    descrizione = additional_detail['descrizione']
                    if 'TICKET' in descrizione:
                        yield cod


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')
    info('select cod where TICKET in descrizione:')
    for cod in sorted(set(all_ticketcods())):
        info('cod: %d', cod)


if __name__ == '__main__':
    main()
