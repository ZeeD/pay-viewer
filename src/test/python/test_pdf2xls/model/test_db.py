'test module test_pdf2xls'

import unittest
import pdf2xls.model.db


class TestDb(unittest.TestCase):
    'test class test_pdf2xls.Db'

    def testEmptyDb(self):
        db = pdf2xls.model.db.Db()
