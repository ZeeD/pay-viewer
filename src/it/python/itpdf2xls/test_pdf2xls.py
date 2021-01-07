'test module pdf2xls'

import datetime
import decimal
import unittest

import mockito
import pdf2xls.model.db
import pdf2xls.model.info
import pdf2xls.model.keys
import pdf2xls.mtime.abcmtimerereader
import pdf2xls.pdf2xls
import pdf2xls.reader.pdfreader

from . import loadResourcePdf


class TestPdf2Xls(unittest.TestCase):
    'test pdf2xls functions'

    def testReadRealPdf(self) -> None:
        'read_infos'

        input_stream = loadResourcePdf(2019, 1)
        mock_mtime_reader = mockito.mock(
            pdf2xls.mtime.abcmtimerereader.ABCMtimeReader)  # type: ignore
        reader = pdf2xls.reader.pdfreader.PdfReader(
            input_stream, mock_mtime_reader)
        db = pdf2xls.model.db.Db()

        pdf2xls.pdf2xls.read_infos(reader, db)

        self.assertEqual({
            pdf2xls.model.keys.Keys.minimo: [
                pdf2xls.model.info.InfoPoint(datetime.date(2019, 1, 1),
                                             decimal.Decimal('2061.41'))
            ],
            pdf2xls.model.keys.Keys.scatti: [
                pdf2xls.model.info.InfoPoint(datetime.date(2019, 1, 1),
                                             decimal.Decimal('109.23'))
            ],
            pdf2xls.model.keys.Keys.superm: [
                pdf2xls.model.info.InfoPoint(datetime.date(2019, 1, 1),
                                             decimal.Decimal('50.87'))
            ],
            pdf2xls.model.keys.Keys.sup_ass: [
                pdf2xls.model.info.InfoPoint(datetime.date(2019, 1, 1),
                                             decimal.Decimal('674.16'))
            ],
            pdf2xls.model.keys.Keys.edr: [
                pdf2xls.model.info.InfoPoint(datetime.date(2019, 1, 1),
                                             decimal.Decimal('0'))
            ],
            pdf2xls.model.keys.Keys.totale_retributivo: [
                pdf2xls.model.info.InfoPoint(datetime.date(2019, 1, 1),
                                             decimal.Decimal('2895.67'))
            ],
            pdf2xls.model.keys.Keys.ferie_a_prec: [
                pdf2xls.model.info.InfoPoint(datetime.date(2019, 1, 1),
                                             decimal.Decimal('-1.82'))
            ],
            pdf2xls.model.keys.Keys.ferie_spett: [
                pdf2xls.model.info.InfoPoint(datetime.date(2019, 1, 1),
                                             decimal.Decimal('1.67'))
            ],
            pdf2xls.model.keys.Keys.ferie_godute: [
                pdf2xls.model.info.InfoPoint(datetime.date(2019, 1, 1),
                                             decimal.Decimal('0'))
            ],
            pdf2xls.model.keys.Keys.ferie_saldo: [
                pdf2xls.model.info.InfoPoint(datetime.date(2019, 1, 1),
                                             decimal.Decimal('-0.15'))
            ],
            pdf2xls.model.keys.Keys.par_a_prec: [
                pdf2xls.model.info.InfoPoint(datetime.date(2019, 1, 1),
                                             decimal.Decimal('594.68'))
            ],
            pdf2xls.model.keys.Keys.par_spett: [
                pdf2xls.model.info.InfoPoint(datetime.date(2019, 1, 1),
                                             decimal.Decimal('8.67'))
            ],
            pdf2xls.model.keys.Keys.par_godute: [
                pdf2xls.model.info.InfoPoint(datetime.date(2019, 1, 1),
                                             decimal.Decimal('0'))
            ],
            pdf2xls.model.keys.Keys.par_saldo: [
                pdf2xls.model.info.InfoPoint(datetime.date(2019, 1, 1),
                                             decimal.Decimal('603.35'))
            ],
            pdf2xls.model.keys.Keys.netto_da_pagare: [
                pdf2xls.model.info.InfoPoint(datetime.date(2019, 1, 1),
                                             decimal.Decimal('2090.00'))
            ]
        }, db.group_infos_by_feature())
