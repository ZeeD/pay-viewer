'test module test_pdf2xls'

import datetime
import decimal
import unittest

import pdf2xls.model.db
import pdf2xls.model.info


class TestDb(unittest.TestCase):
    'test class test_pdf2xls.Db'

    def testEmptyDb(self) -> None:
        'empty db create an empty groups'

        db = pdf2xls.model.db.Db()
        groups = db.group_infos_by_feature()
        self.assertEqual({}, groups)

    def testJustOneInfo(self) -> None:
        db = pdf2xls.model.db.Db()
        db.add_info(pdf2xls.model.info.Info(datetime.datetime(1982, 5, 11),
                                            decimal.Decimal('1'),
                                            'feature'))
        groups = db.group_infos_by_feature()
        self.assertEqual({
            'feature': [
                pdf2xls.model.info.InfoPoint(datetime.datetime(1982, 5, 11),
                                             decimal.Decimal('1'))
            ]
        }, groups)

    def testTwoInfosOneFeature(self) -> None:
        db = pdf2xls.model.db.Db()
        db.add_info(pdf2xls.model.info.Info(datetime.datetime(1982, 5, 11),
                                            decimal.Decimal('1'),
                                            'feature'))
        db.add_info(pdf2xls.model.info.Info(datetime.datetime(1983, 11, 10),
                                            decimal.Decimal('2'),
                                            'feature'))
        groups = db.group_infos_by_feature()
        self.assertEqual({
            'feature': [
                pdf2xls.model.info.InfoPoint(datetime.datetime(1982, 5, 11),
                                             decimal.Decimal('1')),
                pdf2xls.model.info.InfoPoint(datetime.datetime(1983, 11, 10),
                                             decimal.Decimal('2'))
            ]
        }, groups)
