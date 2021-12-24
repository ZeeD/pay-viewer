from pathlib import Path

from .ui import main_window


def main() -> None:
    data_path = Path('C:/Users/ZeDs_/eclipse-workspace/pdf2xls-data')

    with main_window(data_path) as window:
        window.show()


if __name__ == '__main__':
    main()
