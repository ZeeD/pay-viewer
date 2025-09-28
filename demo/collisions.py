#!/usr/bin/env python

from collections import defaultdict
from json import load
from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

LOGGER = getLogger(__name__)

COLLISIONS = defaultdict[int, set[str]](set)
BACKWARD = defaultdict[str, set[int]](set)
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
                COLLISIONS[cod].add(descrizione)
                BACKWARD[descrizione].add(cod)


def collisions() -> None:
    for cod in sorted(COLLISIONS):
        if len(COLLISIONS[cod]) == 1:
            continue
        LOGGER.info(
            'cod: %s, len(COLLISIONS[cod]): %s', cod, len(COLLISIONS[cod])
        )
        for descrizione in sorted(COLLISIONS[cod]):
            LOGGER.info('descrizione: %s', descrizione)


def backwards() -> None:
    for descrizione in sorted(BACKWARD):
        if len(BACKWARD[descrizione]) == 1:
            continue
        LOGGER.info(
            'descrizione: %s, len(BACKWARD[descrizione]): %s',
            descrizione,
            len(BACKWARD[descrizione]),
        )
        for cod in sorted(BACKWARD[descrizione]):
            LOGGER.info('cod: %s', cod)


if __name__ == '__main__':
    basicConfig(level=INFO, format='%(message)s')
    LOGGER.info('------------------collisions')
    collisions()
    LOGGER.info('--------------------backward')
    backwards()
