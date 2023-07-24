from pathlib import Path
from typing import Any
from typing import BinaryIO

from pandas import DataFrame

def read_pdf_with_template(input_path: Path | BinaryIO,
                           template_path: Path | str,
                           *,
                           java_options: list[str] = [],
                           pandas_options: dict[str, Any] = {},
                           multiple_tables: bool = True,
                           guess: bool = True,
                           lattice: bool = False,
                           pages: int | str = 1,
                           stream: bool = False) -> list[DataFrame]:
    ...
