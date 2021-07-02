from pathlib import Path

from .ui import main_window


def main() -> None:
    root = Path(__file__).parent.parent
    file_name = root / 'resources' / 'output.csv'

    with main_window(file_name) as window:
        window.show()


if __name__ == '__main__':
    main()
