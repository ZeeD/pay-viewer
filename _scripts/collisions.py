#!/usr/bin/env python

from collections import defaultdict
from json import load
from pathlib import Path

COLLISIONS = defaultdict[str, set[str]](lambda: set([]))
BACKWARD = defaultdict[str, set[str]](lambda: set([]))
for filename in sorted(Path('../../pdf2xls-data').glob('**/*.pdf.json')):
    with filename.open(encoding='utf-8') as fp:
        for obj in load(fp):
            for additional_detail in obj['additional_details']:
                cod = additional_detail['cod']
                descrizione = additional_detail['descrizione']
                COLLISIONS[cod].add(descrizione)
                BACKWARD[descrizione].add(cod)

def collisions() -> None:
    for cod in sorted(COLLISIONS):
        if len(COLLISIONS[cod]) == 1:
            continue
        print(f'{cod=}, {len(COLLISIONS[cod])=}')
        for descrizione in sorted(COLLISIONS[cod]):
            print(f'\t{descrizione=}')

def backwards() -> None:
    for descrizione in sorted(BACKWARD):
        if len(BACKWARD[descrizione]) == 1:
            continue
        print(f'{descrizione=}, {len(BACKWARD[descrizione])=}')
        for cod in sorted(BACKWARD[descrizione]):
            print(f'\t{cod=}')

if __name__ == '__main__':
    print('------------------collisions')
    collisions()
    print('--------------------backward')
    backwards()
