'main'

import glob
import os.path
import sys
import typing

import pdf2xls.model.db
import pdf2xls.mtime.mtimereader
import pdf2xls.pdf2xls
import pdf2xls.reader.historyreader
import pdf2xls.reader.pdfreader
import pdf2xls.writer.historywriter
import pdf2xls.writer.xlswriter


OUTPUT_XLS = f'{__file__}/../../../../output.xlsx'


def get_file_names(args: typing.List[str]) -> typing.Iterable[str]:
    'glob args'
    for arg in args:
        for file_name in glob.glob(arg):
            yield file_name


def convert_to_pdf_json(file_names: typing.Iterable[str]
                        ) -> typing.Iterable[typing.Tuple[str, str]]:
    'from a list of pdfs to a list of [pdf, json] elements'
    for file_name in file_names:
        yield file_name, f'{file_name}.json'


def get_history_writer(json_file_name: str
                       ) -> pdf2xls.writer.historywriter.HistoryWriter:
    'factory for HistoryWriter'
    json_file = open(json_file_name, 'w')  # not closed!
    return pdf2xls.writer.historywriter.HistoryWriter(json_file)


def get_pdf_reader(pdf_file_name: str
                   ) -> pdf2xls.reader.pdfreader.PdfReader:
    'factory for PdfReader (with some logic to write to history)'
    with open(pdf_file_name, 'rb') as pdf_file:
        mtime_reader = pdf2xls.mtime.mtimereader.MtimeReader(pdf_file)
        pdf_reader = pdf2xls.reader.pdfreader.PdfReader(pdf_file, mtime_reader)

        # copy data into json
        db_ = pdf2xls.model.db.Db()
        pdf2xls.pdf2xls.read_infos(pdf_reader, db_)
        history_writer = get_history_writer(f'{pdf_file_name}.json')
        try:
            pdf2xls.pdf2xls.write_infos(history_writer, db_)
        finally:
            history_writer.close()

        return pdf_reader


def get_history_reader(json_file_name: str
                       ) -> pdf2xls.reader.historyreader.HistoryReader:
    'factory for HistoryReader'
    json_file = open(json_file_name, 'r')
    mtime_reader = pdf2xls.mtime.mtimereader.MtimeReader(json_file)
    return pdf2xls.reader.historyreader.HistoryReader(json_file,
                                                      mtime_reader)


def get_reader(pdf_file_name: str) -> pdf2xls.reader.abcreader.ABCReader:
    'logic to choose from the real pdf or the cached infos'
    json_file_name = f'{pdf_file_name}.json'

    try:
        jf_mtime = os.path.getmtime(json_file_name)
    except FileNotFoundError:
        pass
    else:
        if os.path.getmtime(pdf_file_name) < jf_mtime:
            return get_history_reader(json_file_name)

    return get_pdf_reader(pdf_file_name)


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

    args = sys.argv[1:]
    if not args:
        # autopopulate
        args = [f'{__file__}/../../resources/20*/*.pdf']

    db_ = pdf2xls.model.db.Db()

    for pdf_file_name in get_file_names(args):
        reader = get_reader(pdf_file_name)
        pdf2xls.pdf2xls.read_infos(reader, db_)

    with open(OUTPUT_XLS, 'wb') as xls_file:
        xls_writer = pdf2xls.writer.xlswriter.XlsWriter(xls_file)
        try:
            pdf2xls.pdf2xls.write_infos(xls_writer, db_)
        finally:
            xls_writer.close()


if __name__ == '__main__':
    main()
