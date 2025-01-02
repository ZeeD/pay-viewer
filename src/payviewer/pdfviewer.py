from typing import TYPE_CHECKING

from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView

if TYPE_CHECKING:
    from pathlib import Path

    from PySide6.QtWidgets import QWidget


def view_pdf(path: 'Path') -> 'QWidget':
    pdf_path = str(path.with_suffix('') if path.suffix == '.json' else path)

    view = QPdfView()
    document = QPdfDocument(view)
    document.load(pdf_path)
    view.setDocument(document)
    view.setPageMode(QPdfView.PageMode.SinglePage)
    view.setZoomMode(QPdfView.ZoomMode.FitToWidth)
    return view
