from os import remove
from pathlib import Path


def main() -> None:
    root = Path(__file__).parent.parent

    for file_name in (root / 'resources').glob('20*/*.pdf.json'):
        remove(file_name)


if __name__ == '__main__':
    main()
