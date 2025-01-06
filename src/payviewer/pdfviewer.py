from typing import TYPE_CHECKING

from PySide6.QtGui import QGuiApplication
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

    scren_size = QGuiApplication.primaryScreen().size()
    view.resize(scren_size.width() // 2, scren_size.height() // 2)
    view.setWindowTitle(pdf_path)

    return view
