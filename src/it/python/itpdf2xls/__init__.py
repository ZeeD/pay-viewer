from pathlib import Path


def loadResourcePdf(year: int, month: int) -> str:
    'load a pdf from the resources path'
    here = Path(__file__).parent
    p = here / '..' / '..' / 'resources' / \
        f'{year:04}' / f'Cedolini_{year:04}_{month:02}.pdf'
    return str(p)


def resourceXls(filename: str) -> str:
    'open a writable file to a xls from the resources path'
    here = Path(__file__).parent
    p = here / '..' / '..' / 'resources' / 'outxls' / f'{filename}.xlsx'
    return str(p)
