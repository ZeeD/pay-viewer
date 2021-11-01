from typing import List

from .cli import parse_args
from .loader import get_reader
from .mainui import main_ui
from .model import Info
from .writer.csvwriter import CsvWriter
from .writer.xlswriter import XlsWriter


def old_main() -> None:
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


main = main_ui

if __name__ == '__main__':
    main()
