from argparse import ArgumentParser, Namespace
from pathlib import Path

PDF2XLS_DATA_ROOT = Path(__file__).parent.parent.parent / 'pdf2xls-data'


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('--output_dir',
                        metavar='output-dir',
                        default=PDF2XLS_DATA_ROOT)
    parser.add_argument('pdf_file',
                        nargs='*',
                        metavar='pdf-file',
                        default=list(PDF2XLS_DATA_ROOT.glob('*/*.pdf')))
    return parser.parse_args()
