import io


class PdfFileReader:

    def __init__(self, file:io.RawIOBase) -> None:
        ...

    def getPage(self, page:int) -> Page:
        ...


class Page:

    def extractText() -> str:
        ...
