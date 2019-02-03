'main'

import sys

from pdf2xls.model import Db
from pdf2xls.reader import HistoryReader, PdfReader
from pdf2xls.writer import XlsWriter
import typing


def main() -> None:
    'entry point'

    args = sys.argv[1:]

    history_reader = HistoryReader()
    pdf_reader = PdfReader()
    xml_writer = XlsWriter()

    db = Db()

    return pdf2xml(args, history_reader, pdf_reader, xml_writer, db)


def pdf2xml(args: typing.List[str],
            history_reader: HistoryReader,
            pdf_reader: PdfReader,
            xls_writer: XlsWriter,
            db: Db):
    'pdf2xml'

    for historic_info in history_reader.read_infos(None):
        db.add_info(historic_info)

    for file_name in args:
        with open(file_name) as pdf_file:
            for pdf_info in pdf_reader.read_infos(pdf_file):
                db.add_info(pdf_info)

    with open('output.xml', 'wb') as xml_file:
        xls_writer.write_infos(db.get_all_infos(), xml_file)


if __name__ == '__main__':
    main()
