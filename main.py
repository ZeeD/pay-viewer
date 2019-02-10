'main'

import sys

import pdf2xls.model.db
import pdf2xls.pdf2xls
import pdf2xls.reader.historyreader
import pdf2xls.reader.pdfreader
import pdf2xls.writer.xlswriter

HISTORY_DAT = 'history.dat'
OUTPUT_XML = 'output.xml'


def main() -> None:
    'entry point'

    args = sys.argv[1:]

    history_reader = pdf2xls.reader.historyreader.HistoryReader()
    pdf_reader = pdf2xls.reader.pdfreader.PdfReader()
    xls_writer = pdf2xls.writer.xlswriter.XlsWriter()

    db = pdf2xls.model.db.Db()

    with open(HISTORY_DAT, 'rb') as history_file:
        pdf2xls.pdf2xls.read_infos(history_file, history_reader, db)

    for file_name in args:
        with open(file_name, 'rb') as pdf_file:
            pdf2xls.pdf2xls.read_infos(pdf_file, pdf_reader, db)

    with open(OUTPUT_XML, 'wb') as xls_file:
        pdf2xls.pdf2xls.write_infos(xls_file, xls_writer, db)


if __name__ == '__main__':
    main()
