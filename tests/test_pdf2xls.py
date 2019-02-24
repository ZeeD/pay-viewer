'test module pdf2xls'

import typing
import unittest

import mockito

import pdf2xls.model.db
import pdf2xls.pdf2xls
import pdf2xls.reader.abcreader
import pdf2xls.writer.abcwriter


class TestPdf2Xls(unittest.TestCase):
    'test pdf2xls functions'

    def testReadInfos(self) -> None:
        'read_infos'

        input_stream = mockito.mock(typing.BinaryIO)
        reader = mockito.mock(pdf2xls.reader.abcreader.ABCReader)
        db = mockito.mock(pdf2xls.model.db.Db)

        mockito.when(reader).read_infos(input_stream).thenReturn([])

        pdf2xls.pdf2xls.read_infos(input_stream, reader, db)

    def testWriteInfos(self) -> None:
        'write_infos'

        output_stream = mockito.mock(typing.BinaryIO)
        writer = mockito.mock(pdf2xls.writer.abcwriter.ABCWriter)
        db = mockito.mock(pdf2xls.model.db.Db)

        mockito.when(db).group_infos_by_feature().thenReturn({})

        pdf2xls.pdf2xls.write_infos(output_stream, writer, db)
