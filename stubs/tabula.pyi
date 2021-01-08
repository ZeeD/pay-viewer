import typing
import pandas


def read_pdf_with_template(input_path: typing.BinaryIO,
                           template_path: str,
                           *,
                           java_options: typing.List[str] = [],
                           pandas_options: typing.Dict[str, typing.Any] = {},
                           multiple_tables: bool = True,
                           guess: bool = True,
                           lattice: bool = False,
                           pages: typing.Union[int, str]=1,
                           stream: bool = False
                           ) -> typing.List[pandas.DataFrame]:
    ...
