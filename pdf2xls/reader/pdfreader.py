'pdf reader'

import io
import typing

import pdfminer3.high_level
import pdfminer3.layout

from . import abcreader
from ..model import info


class PdfReader(abcreader.ABCReader):
    'retrieve infos from .pdf'

    def read_infos(self,
                   info_file: typing.BinaryIO
                   ) -> typing.Iterable[info.Info]:
        'read from a file'

        laparams = pdfminer3.layout.LAParams(detect_vertical=True,
                                             all_texts=True)

        outf = io.StringIO()
        pdfminer3.high_level.extract_text_to_fp(info_file, outf,
                                                laparams=laparams,
                                                debug=True)
        outf.flush()
        outf.seek(0)
        text = outf.read()
        rows = [ row for row in text.split('\n') if row and row.strip() ]
        print(text)

        return []
