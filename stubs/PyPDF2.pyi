'stub for PyPDF2'

import typing

class Page:

    def extractText(self) -> str:
        'extractText'


class PdfFileReader:

    def __init__(self,
                 file: typing.BinaryIO
                 ) -> None:
        '__init__'

    def getPage(self,
                page: int
                ) -> Page:
        'getPage'

