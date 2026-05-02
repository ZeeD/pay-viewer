from logging import INFO
from logging import basicConfig
from logging import getLogger
from sys import argv

from payviewer.settings import Settings

logger = getLogger(__name__)


def dump(settings: Settings, prefix: str = '') -> None:
    logger.info('%susername: %s', prefix, settings.username)
    logger.info('%spassword: %s', prefix, settings.password)
    logger.info('%sdata_path: %s', prefix, settings.data_path)


def set_password(settings: Settings, password: str) -> None:
    dump(settings, 'orig ')
    settings.password = password
    dump(settings, 'new  ')


def set_data_path(settings: Settings, data_path: str) -> None:
    dump(settings, 'orig ')
    settings.data_path = data_path
    dump(settings, 'new  ')


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')

    arg, *args = argv

    settings = Settings()
    if not args or args in (['-d'], ['--dump']):
        dump(settings)
    elif args[0] in ('-P', '--password') and len(args) == 2:  # noqa:PLR2004
        set_password(settings, args[1])
    elif args[0] in ('-p', '--data-path') and len(args) == 2:  # noqa:PLR2004
        set_data_path(settings, args[1])
    else:  # usage
        logger.warning('uso: %s [-d] | [-P password] | [-p path]', arg)


if __name__ == '__main__':
    main()
