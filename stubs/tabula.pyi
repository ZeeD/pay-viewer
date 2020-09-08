'stub for tabula'

import typing
import pandas


def read_pdf(input_path: typing.BinaryIO,
             *,
             java_options: typing.List[str] = [],
             pandas_options: typing.Dict[str, typing.Any] = {},
             multiple_tables: bool = True,
             guess: bool = True,
             lattice: bool = False,
             pages: typing.Union[int, str]=1
             ) -> typing.List[pandas.DataFrame]:
    'read_pdf'
