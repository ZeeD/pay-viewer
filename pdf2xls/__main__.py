from os.path import getmtime
from pathlib import Path
from typing import List

from .model import Info
from .reader.abcreader import ABCReader
from .reader.historyreader import HistoryReader
from .reader.pdfreader import PdfReader
from .writer.csvwriter import CsvWriter
from .writer.historywriter import HistoryWriter
from .writer.xlswriter import XlsWriter
from .cli import parse_args


def _create_json_from_pdf(pdf_file_name: Path) -> None:
    infos = PdfReader(pdf_file_name).read_infos()
    HistoryWriter(pdf_file_name.with_suffix('.pdf.json')).write_infos(infos)


def get_reader(pdf_file_name: Path) -> ABCReader:
    try:
        history_mtime = getmtime(pdf_file_name.with_suffix('.pdf.json'))
    except FileNotFoundError:
        _create_json_from_pdf(pdf_file_name)
    else:
        if history_mtime < getmtime(pdf_file_name):
            _create_json_from_pdf(pdf_file_name)

    return HistoryReader(pdf_file_name.with_suffix('.pdf.json'))


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

    ns = parse_args()

    infos: List[Info] = []
    for name in ns.pdf_file:
        infos.extend(get_reader(name).read_infos())

    XlsWriter(ns.output_dir / 'output.xlsx').write_infos(infos)
    CsvWriter(ns.output_dir / 'output.csv').write_infos(infos)


if __name__ == '__main__':
    main()
