import argparse
import sys
from typing import Union

from webshot import __version__


class Characters:
    ERROR = '\u0445'
    OK = '\u221a'
    INFO = '\u25cf'


class Color:
    OK = '\033[92m'
    WARN = '\033[93m'
    ERROR = '\033[91m'
    INFO = '\033[94m'
    BANNER = '\033[94m'
    CYAN = '\033[96m'
    DEFAULT = '\033[0m'


def get_config() -> tuple:
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-v', '--version',
                           action='version',
                           version='%(prog)s {}'.format(__version__))
    argparser.add_argument('-o', '--output',
                           action='store',
                           help='output directory',
                           default='./webshot_report')
    argparser.add_argument('-t', '--threads',
                           action='store',
                           type=int,
                           default=5,
                           help='number of threads')
    args = argparser.parse_args()
    return args.output, args.threads


def get_domains() -> Union[list, None]:
    return [_.replace('\n', '') for _ in sys.stdin.readlines()] if not sys.stdin.isatty() else None


def banner() -> None:
    print(f"""{Color.BANNER}
     __          __  _     _____ _           _   
     \ \        / / | |   / ____| |         | |  
      \ \  /\  / /__| |__| (___ | |__   ___ | |_ 
       \ \/  \/ / _ \ '_  \___ \| '_ \ / _ \| __|
        \  /\  /  __/ |_) |___) | | | | (_) | |_ 
         \/  \/ \___|_.__/_____/|_| |_|\___/ \__|

        ver {__version__}{Color.DEFAULT}
    """)


def info(msg) -> None:
    print(f"{Color.INFO}{Characters.INFO}{Color.DEFAULT} {msg}")


def error(msg) -> None:
    print(f"{Color.ERROR}{Characters.ERROR}{Color.DEFAULT} {msg}")


def ok(msg) -> None:
    print(f"{Color.OK}{Characters.OK}{Color.DEFAULT} {msg}")
