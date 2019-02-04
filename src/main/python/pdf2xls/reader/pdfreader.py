'pdf reader'

import io
import typing

import PyPDF2

from ..model import Info
from .abcreader import ABCReader


class PdfReader(ABCReader):
    'retrieve infos from .pdf'

    def read_infos(self,
                   info_file: typing.Optional[io.RawIOBase]
                   ) -> typing.Iterable[Info]:
        'read from a file'

        if info_file is None:
            raise Exception('you must pass a file')

        pdfReader = PyPDF2.PdfFileReader(info_file)
        pageObj = pdfReader.getPage(0)
        text = pageObj.extractText()
        print(text)

        return []
