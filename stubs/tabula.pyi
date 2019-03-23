'stub for tabula'

import typing
import pandas


def read_pdf(input_path: typing.BinaryIO,
             *,
             multiple_tables: bool,
             java_options: typing.List[str],
             guess: bool,
             lattice: bool
             ) -> typing.List[pandas.DataFrame]:
    'read_pdf'
