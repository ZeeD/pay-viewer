from typing import Literal

def setup(name: str,
          version: str,
          description: str,
          url: str,
          author: str,
          author_email: str,
          license: str,
          packages: list[str],
          zip_safe: bool,
          install_requires: list['str'],
          entry_points: dict[Literal['console_scripts', 'gui_scripts'], list[str]]) -> None:
    ...


def find_packages() -> list[str]: ...
