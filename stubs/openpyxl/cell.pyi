from datetime import date
from decimal import Decimal

from openpyxl.worksheet.worksheet import Worksheet

class Cell:
    number_format: str
    column_letter: str
    value: str | date | Decimal | None

    def __init__(
        self, worksheet: Worksheet, value: str | date | Decimal | None = None
    ) -> None: ...
