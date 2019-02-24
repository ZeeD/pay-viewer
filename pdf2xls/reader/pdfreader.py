'pdf reader'

import datetime
import decimal
import io
import typing

import pdfminer3.high_level
import pdfminer3.layout

from . import abcreader
from ..model import info
from ..model import keys


class PdfReader(abcreader.ABCReader):
    'retrieve infos from .pdf'

    def read_infos(self,
                   info_file: typing.BinaryIO
                   ) -> typing.Iterable[info.Info]:
        'read from a file'

        laparams = pdfminer3.layout.LAParams(detect_vertical=True,
                                             all_texts=True)

        with io.StringIO() as outf:
            pdfminer3.high_level.extract_text_to_fp(info_file, outf,
                                                    laparams=laparams)
            outf.seek(0)
            rows = [row for row in outf.readlines() if row and row.strip()]

        when = extract_periodo(rows)

        minimo = extract_minimo(rows)
        scatti = extract_scatti(rows)
        superm = extract_superm(rows)
        sup_ass = extract_sup_ass(rows)
        totale_retributivo = extract_totale_retributivo(rows)

        return [
            info.Info(when, minimo, keys.Keys.minimo),
            info.Info(when, scatti, keys.Keys.scatti),
            info.Info(when, superm, keys.Keys.superm),
            info.Info(when, sup_ass, keys.Keys.sup_ass),
            info.Info(when, totale_retributivo, keys.Keys.totale_retributivo)
        ]


def extract_periodo(rows: typing.List[str]) -> datetime.datetime:
    'extract the right row, and parse the date inside'

    words = rows[11].split()

    month = {
        'GENNAIO': 1, 'FEBBRAIO': 2, 'MARZO': 3, 'APRILE': 4, 'MAGGIO': 5,
        'GIUGNO': 6, 'LUGLIO': 7, 'AGOSTO': 8, 'SETTEMBRE': 9, 'OTTOBRE': 10,
        'NOVEMBRE': 11, 'DICEMBRE': 12
    }[words[1]]
    year = int(words[2])

    return datetime.datetime(year, month, 1)


def extract_minimo(rows: typing.List[str]) -> decimal.Decimal:
    return decimal.Decimal(rows[26].split()[0].replace(',', '.'))


def extract_scatti(rows: typing.List[str]) -> decimal.Decimal:
    return decimal.Decimal(rows[26].split()[1].replace(',', '.'))


def extract_superm(rows: typing.List[str]) -> decimal.Decimal:
    return decimal.Decimal(rows[27].split()[0].replace(',', '.'))


def extract_sup_ass(rows: typing.List[str]) -> decimal.Decimal:
    return decimal.Decimal(rows[28].split()[0].replace(',', '.'))


def extract_totale_retributivo(rows: typing.List[str]) -> decimal.Decimal:
    return decimal.Decimal(rows[30].split()[0].replace('.', '').replace(',', '.'))
