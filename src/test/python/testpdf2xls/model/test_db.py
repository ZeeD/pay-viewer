'test module test_pdf2xls'

import datetime
import decimal
import unittest

import pdf2xls.model.db
import pdf2xls.model.info
import pdf2xls.model.keys


class TestDb(unittest.TestCase):
    'test class test_pdf2xls.Db'

    def testEmptyDb(self) -> None:
        'empty db create an empty groups'

        db = pdf2xls.model.db.Db()
        groups = db.group_infos_by_feature()
        self.assertEqual({}, groups)

    def testJustOneInfo(self) -> None:
        db = pdf2xls.model.db.Db()
        db.add_info(pdf2xls.model.info.Info(datetime.date(1982, 5, 11),
                                            decimal.Decimal('1'),
                                            pdf2xls.model.keys.Keys.minimo))
        groups = db.group_infos_by_feature()
        self.assertEqual({
            pdf2xls.model.keys.Keys.minimo: [
                pdf2xls.model.info.InfoPoint(datetime.date(1982, 5, 11),
                                             decimal.Decimal('1'))
            ]
        }, groups)

    def testTwoInfosOneFeature(self) -> None:
        db = pdf2xls.model.db.Db()
        db.add_info(pdf2xls.model.info.Info(datetime.date(1982, 5, 11),
                                            decimal.Decimal('1'),
                                            pdf2xls.model.keys.Keys.minimo))
        db.add_info(pdf2xls.model.info.Info(datetime.date(1983, 11, 10),
                                            decimal.Decimal('2'),
                                            pdf2xls.model.keys.Keys.minimo))
        groups = db.group_infos_by_feature()
        self.assertEqual({
            pdf2xls.model.keys.Keys.minimo: [
                pdf2xls.model.info.InfoPoint(datetime.date(1982, 5, 11),
                                             decimal.Decimal('1')),
                pdf2xls.model.info.InfoPoint(datetime.date(1983, 11, 10),
                                             decimal.Decimal('2'))
            ]
        }, groups)
