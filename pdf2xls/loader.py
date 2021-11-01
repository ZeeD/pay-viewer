from os.path import getmtime
from pathlib import Path
from typing import List

from .model import Info
from .reader.abcreader import ABCReader
from .reader.historyreader import HistoryReader
from .reader.pdfreader import PdfReader
from .writer.historywriter import HistoryWriter


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


def load(data_path: str) -> List[Info]:
    infos: List[Info] = []
    for name in Path(data_path).glob('*/*.pdf'):
        infos.extend(get_reader(name).read_infos())
    return infos
