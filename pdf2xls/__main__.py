from glob import glob
from os.path import getmtime
from sys import argv
from typing import List

from .model import Info
from .reader.abcreader import ABCReader
from .reader.historyreader import HistoryReader
from .reader.pdfreader import PdfReader
from .writer.historywriter import HistoryWriter
from .writer.xlswriter import XlsWriter


def _create_json_from_pdf(pdf_file_name: str) -> None:
    infos = PdfReader(pdf_file_name).read_infos()
    HistoryWriter(f'{pdf_file_name}.json').write_infos(infos)


def get_reader(pdf_file_name: str) -> ABCReader:
    try:
        history_mtime = getmtime(f'{pdf_file_name}.json')
    except FileNotFoundError:
        _create_json_from_pdf(pdf_file_name)
    else:
        if history_mtime < getmtime(pdf_file_name):
            _create_json_from_pdf(pdf_file_name)

    return HistoryReader(f'{pdf_file_name}.json')


def main() -> None:
    '''usage: pdf2xml *.pdf
    * create an 'output.xlsx' file
    * create a '*.pdf.json' for each input
    * behaviour:
    * for each PDF:
    *   if a PDF_JSON exists and mtime(PDF) < mtime(PDF_JSON):
    *       read from PDF_JSON
    *   else:
    *       read from PDF
    *       store into PDF_JSON
    *   mix the data
    *   store into XLSX
    '''

    infos: List[Info] = []
    for arg in argv[1:] or [
            f'{__file__}/../../resources/20*/*.pdf']:  # fallback
        for name in glob(arg):
            infos.extend(get_reader(name).read_infos())

    XlsWriter(f'{__file__}/../../../../output.xlsx').write_infos(infos)


if __name__ == '__main__':
    main()
