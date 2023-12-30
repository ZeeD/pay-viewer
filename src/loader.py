from operator import attrgetter
from pathlib import Path

from model import Info
from reader.abcreader import ABCReader
from reader.historyreader import HistoryReader
from reader.pdfreader import PdfReader
from writer.historywriter import HistoryWriter


class NoHistoryError(Exception):
    ...


def _create_json_from_pdf(pdf_file_name: Path) -> None:
    infos = PdfReader(pdf_file_name).read_infos()
    HistoryWriter(pdf_file_name.with_suffix('.pdf.json')).write_infos(infos)


def _get_reader(pdf_file_name: Path, *, force: bool) -> ABCReader:
    try:
        history_mtime = pdf_file_name.with_suffix('.pdf.json').stat().st_mtime
    except FileNotFoundError as e:
        if not force:
            raise NoHistoryError(pdf_file_name) from e
        _create_json_from_pdf(pdf_file_name)
    else:
        if history_mtime < pdf_file_name.stat().st_mtime:
            _create_json_from_pdf(pdf_file_name)

    return HistoryReader(pdf_file_name.with_suffix('.pdf.json'))


def load(data_path: str, *, force: bool = False) -> list[Info]:
    infos: list[Info] = []
    for name in Path(data_path).glob('*/*.pdf'):
        infos.extend(_get_reader(name, force=force).read_infos())
    infos.sort(key=attrgetter('when'))
    return infos
