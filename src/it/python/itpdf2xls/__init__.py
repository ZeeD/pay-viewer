'support for tests'

import pathlib
import typing


def loadResourcePdf(year: int, month: int) -> typing.BinaryIO:
    'load a pdf from the resources path'
    here = pathlib.Path(__file__).parent
    p = here / '..' / '..' / 'resources' / \
        f'{year:04}' / f'Cedolini_{year:04}_{month:02}.pdf'
    return p.open('rb')


def resourceXls(filename: str) -> typing.BinaryIO:
    'open a writable file to a xls from the resources path'
    here = pathlib.Path(__file__).parent
    p = here / '..' / '..' / 'resources' / 'outxls' / f'{filename}.xlsx'
    return p.open('wb')
