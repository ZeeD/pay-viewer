from pathlib import Path
from typing import Any
from typing import BinaryIO
from typing import Union

from pandas import DataFrame

def read_pdf_with_template(input_path: Union[Path, BinaryIO],
                           template_path: Union[Path, str],
                           *,
                           java_options: list[str] = [],
                           pandas_options: dict[str, Any] = {},
                           multiple_tables: bool = True,
                           guess: bool = True,
                           lattice: bool = False,
                           pages: Union[int, str] = 1,
                           stream: bool = False) -> list[DataFrame]:
    ...
