'pdf reader'

import typing

import PyPDF2

from . import abcreader
from ..model import info


class PdfReader(abcreader.ABCReader):
    'retrieve infos from .pdf'

    def read_infos(self,
                   info_file: typing.BinaryIO
                   ) -> typing.Iterable[info.Info]:
        'read from a file'

        pdfReader = PyPDF2.PdfFileReader(info_file)
        pageObj = pdfReader.getPage(0)
        text = pageObj.extractText()
        print(text)

        return []
