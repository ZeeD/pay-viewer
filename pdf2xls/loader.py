from os.path import getmtime
from pathlib import Path

from .model import Info
from .reader.abcreader import ABCReader
from .reader.historyreader import HistoryReader
from .reader.pdfreader import PdfReader
from .writer.historywriter import HistoryWriter


class NoHistoryException(Exception):
    ...


def _create_json_from_pdf(pdf_file_name: Path) -> None:
    infos = PdfReader(pdf_file_name).read_infos()
    HistoryWriter(pdf_file_name.with_suffix('.pdf.json')).write_infos(infos)


def _get_reader(pdf_file_name: Path, force: bool) -> ABCReader:
    try:
        history_mtime = getmtime(pdf_file_name.with_suffix('.pdf.json'))
    except FileNotFoundError as e:
        if not force:
            raise NoHistoryException(pdf_file_name) from e
        _create_json_from_pdf(pdf_file_name)
    else:
        if history_mtime < getmtime(pdf_file_name):
            _create_json_from_pdf(pdf_file_name)

    return HistoryReader(pdf_file_name.with_suffix('.pdf.json'))


def load(data_path: str, *, force: bool = False) -> list[Info]:
    infos: list[Info] = []
    for name in Path(data_path).glob('*/*.pdf'):
        infos.extend(_get_reader(name, force).read_infos())
    return infos
