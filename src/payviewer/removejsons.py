from pathlib import Path


def remove_jsons(data_path: str) -> None:
    for file_name in Path(data_path).glob('*/Cedolini_*_*.pdf.json'):
        file_name.unlink()
