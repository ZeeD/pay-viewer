from PySide6.QtWidgets import QApplication

from pdf2xls.freezetableview import FreezeTableView
from pdf2xls.settings import Settings
from pdf2xls.viewmodel import SortFilterViewModel


app = QApplication([__file__])

settings = Settings()

model = SortFilterViewModel(settings)
ftw = FreezeTableView(None, model)
ftw.show()

model.update(only_local=True, force_pdf=False)

raise SystemExit(app.exec())
