from typing import Any
from typing import BinaryIO
from typing import Dict
from typing import List
from typing import Union

from pandas import DataFrame
from pathlib import Path

def read_pdf_with_template(input_path: Union[Path, BinaryIO],
                           template_path: Path,
                           *,
                           java_options: List[str]=[],
                           pandas_options: Dict[str, Any]={},
                           multiple_tables: bool=True,
                           guess: bool=True,
                           lattice: bool=False,
                           pages: Union[int, str]=1,
                           stream: bool=False) -> List[DataFrame]:
    ...
