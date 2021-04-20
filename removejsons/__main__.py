'removejsons'

import glob
import os


def main() -> None:
    '''usage: removejsons'''

    for file_name in glob.glob(f'{__file__}/../../resources/20*/*.pdf.json'):
        os.remove(file_name)


if __name__ == '__main__':
    main()
