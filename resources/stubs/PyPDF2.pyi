import io


class PdfFileReader:

    def __init__(self, file: typing.BinaryIO) -> None:
        ...

    def getPage(self, page: int) -> Page:
        ...


class Page:

    def extractText(self) -> str:
        ...
