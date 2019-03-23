'stub for mockito'

import typing

from pdfminer3 import layout


def extract_text_to_fp(info_file: typing.BinaryIO,
                          outf: typing.TextIO,
                          laparams: layout.LAParams) -> None:
    'extract_text_to_fp'
