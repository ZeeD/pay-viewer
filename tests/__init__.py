'support for tests'

import pathlib
import typing


def loadResourcePdf(year: int, month: int) -> typing.BinaryIO:
    'load a pdf from the resources path'
    here = pathlib.Path(__file__).parent
    p = here / '..' / 'resources' / f'{year:04}' / f'{month:02}.pdf'
    return p.open('rb')
