'test module pdf2xls'

import datetime
import decimal
import typing
import unittest

import mockito

import pdf2xls.model.db
import pdf2xls.model.info
import pdf2xls.model.keys
import pdf2xls.pdf2xls
import pdf2xls.reader.abcreader
import pdf2xls.reader.pdfreader
import pdf2xls.writer.abcwriter

from . import loadResourcePdf


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

    def testReadRealPdf(self) -> None:
        'read_infos'

        input_stream = loadResourcePdf(2019, 1)
        reader = pdf2xls.reader.pdfreader.PdfReader()
        db = pdf2xls.model.db.Db()

        pdf2xls.pdf2xls.read_infos(input_stream, reader, db)

        self.assertEqual({
            pdf2xls.model.keys.Keys.minimo: [
                pdf2xls.model.info.InfoPoint(datetime.datetime(2019, 1, 1),
                                             decimal.Decimal('2061.41'))
            ],
            pdf2xls.model.keys.Keys.scatti: [
                pdf2xls.model.info.InfoPoint(datetime.datetime(2019, 1, 1),
                                             decimal.Decimal('109.23'))
            ],
            pdf2xls.model.keys.Keys.superm: [
                pdf2xls.model.info.InfoPoint(datetime.datetime(2019, 1, 1),
                                             decimal.Decimal('50.87'))
            ],
            pdf2xls.model.keys.Keys.sup_ass: [
                pdf2xls.model.info.InfoPoint(datetime.datetime(2019, 1, 1),
                                             decimal.Decimal('674.16'))
            ],
            pdf2xls.model.keys.Keys.totale_retributivo: [
                pdf2xls.model.info.InfoPoint(datetime.datetime(2019, 1, 1),
                                             decimal.Decimal('2895.67'))
            ]
        }, db.group_infos_by_feature())
