import os
import sys
import logging
from importlib import reload
from logging import config
from typing import Optional, Dict

from colorama import Fore, Back, Style, init


class ColoredFormatter(logging.Formatter):
    """Colored log formatter."""

    def __init__(
        self, *args, colors: Optional[Dict[str, str]] = None, **kwargs
    ) -> None:
        """Initialize the formatter with specified format strings."""

        super().__init__(*args, **kwargs)

        self.colors = colors if colors else {}

    def format(self, record) -> str:
        """Format the specified record as text."""

        record.color = self.colors.get(record.levelname, "")
        record.reset = Style.RESET_ALL

        return super().format(record)


def get_logger(
    level="info",
    logfile=None,
    logfilemode="a",
    loggingmode="short",
    format_str=None,
    file_format_str=None,
    format_date=None,
    colors=None,
    logger_config=None,
):
    """
    returns Python logging based logger formatted with colors

    :param level: (DEFAULT='info') str of logging level, each str option is mapped to Python logging levels, str options:
                        'info': logging.INFO,
                        'debug': logging.DEBUG,
                        'warning': logging.WARNING,
                        'error': logging.ERROR,
                        'critical': logging.CRITICAL,
                        'notset': logging.NOTSET
    :param logfile: (DEFAULT=None) str path where to save log file, example: '/tmp/my_log.log'
    :param logfilemode: (DEFAULT='a') str of log file writing mode, same as the ones documented at Python logging package. options:
                        'a': appends to logfile
                        'w': overwrites logfile
    :param loggingmode: (DEFAULT='short') str logging mode to be selected. options:
                        'short': will use short str format ('%(asctime)s %(funcName)s,%(lineno)s| %(message)s') and short date format ('%H:%M:%S')
                        'medium': will use long str format ('%(asctime)s | %(filename)s | %(funcName)s,%(lineno)s | %(message)s') and long date format ('%Y-%m-%d %H:%M:%S')
                        'manual': you need to set :param format_str: and :param format_date: yourself
    :param format_str: (DEFAULT=None) str of format logging string for console, only set this if you selected :param loggingmode: as 'manual'. example (the style is always '%', see python logging module for more info):
                        '%(asctime)s | %(filename)s | %(funcName)s,%(lineno)s | %(message)s'
    :param file_format_str: (DEFAULT=None) str of format logging string for logfile (if you keep it None, we will use what you passed in :param format_str:), only set this if you selected :param loggingmode: as 'manual'. example (the style is always '%', see python logging module for more info):
                        '%(asctime)s | %(filename)s | %(funcName)s,%(lineno)s | %(message)s'
    :param date_str: (DEFAULT=None) str of date logging string, only set this if you selected :param loggingmode: as 'manual'. example:
                        '%Y-%m-%d %H:%M:%S'
    :param colors: (DEFAULT=None) dict of color settings, only set this if you selected :param loggingmode: as 'manual'. example:
                        {
                            'DEBUG': Fore.CYAN + Style.BRIGHT,
                            'INFO': Fore.GREEN + Style.BRIGHT,
                            'WARNING': Fore.YELLOW + Style.BRIGHT,
                            'ERROR': Fore.RED + Style.BRIGHT,
                            'CRITICAL': Fore.RED + Back.WHITE + Style.BRIGHT,
                        }
    :param logger_config: (DEFAULT=None) dict python logger config if you want to fully overwrite configs. example:
                        {
                            "version": 1,
                            "disable_existing_loggers": False,
                            "formatters": {
                                "qlog": {
                                    "()": "qlogging.qlogging.ColoredFormatter",
                                    "colors":  {
                                        'DEBUG': Fore.CYAN + Style.BRIGHT,
                                        'INFO': Fore.GREEN + Style.BRIGHT,
                                        'WARNING': Fore.YELLOW + Style.BRIGHT,
                                        'ERROR': Fore.RED + Style.BRIGHT,
                                        'CRITICAL': Fore.RED + Back.WHITE + Style.BRIGHT,
                                    },
                                    "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                                    "datefmt":'%H:%M:%S'
                                },
                            },
                            "handlers": {
                                "console": {
                                    "level": "DEBUG",
                                    "formatter": "qlog",
                                    "class": "logging.StreamHandler",
                                    "stream": "ext://sys.stdout",
                                },
                            },
                            "loggers": {
                                "": {
                                    "handlers": ["console"],
                                    "level": "DEBUG",
                                    "propagate": True,
                                },
                            },
                        }
    :return: formated Python logging instance
    """
    if loggingmode == "short":
        file_format_str = "%(asctime)s %(funcName)s,%(lineno)s| %(message)s"
        format_str = "%(color)s"+file_format_str+"%(reset)s"
        format_date = "%H:%M:%S"
        colors = {
            "DEBUG": Fore.CYAN + Style.BRIGHT,
            "INFO": Fore.GREEN + Style.BRIGHT,
            "WARNING": Fore.YELLOW + Style.BRIGHT,
            "ERROR": Fore.RED + Style.BRIGHT,
            "CRITICAL": Fore.RED + Back.WHITE + Style.BRIGHT,
        }
    elif loggingmode == "long":
        file_format_str = "%(asctime)s | %(filename)s | %(funcName)s,%(lineno)s | %(message)s"
        format_str = "%(color)s"+file_format_str+"%(reset)s"
        format_date = "%Y-%m-%d %H:%M:%S"
        colors = {
            "DEBUG": Fore.CYAN + Style.BRIGHT,
            "INFO": Fore.GREEN + Style.BRIGHT,
            "WARNING": Fore.YELLOW + Style.BRIGHT,
            "ERROR": Fore.RED + Style.BRIGHT,
            "CRITICAL": Fore.RED + Back.WHITE + Style.BRIGHT,
        }
    elif loggingmode == "manual":
        if file_format_str == None: 
            file_format_str = format_str
        format_str = '%(color)s'+format_str+"%(reset)s"
    else:
        print(
            " + Error, unknown logging mode {}, please choose: short/long/manual".format(
                loggingmode
            )
        )

    # reseting current logger config
    logging.handlers = []

    formatter = ColoredFormatter(
        format_str, style="%", datefmt=format_date, colors=colors
    )
    file_formatter = ColoredFormatter(
        file_format_str, style="%", datefmt=format_date, colors=colors
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.handlers[:] = []
    if logfile != None:
        file = logging.FileHandler(logfile, mode=logfilemode)
        file.setFormatter(file_formatter)
        logger.addHandler(file)
    logger.addHandler(handler)

    levels = {
        "info": logging.INFO,
        "debug": logging.DEBUG,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
        "notset": logging.NOTSET,
    }

    logger.setLevel(levels.get(level))
    try:
        if logger_config != None:
            for k, v in logger_config.get("formatters").items():
                if logger_config.get("formatters").get(k).get("format"):
                    if not "color" in logger_config.get("formatters").get(k).get(
                        "format"
                    ):
                        current_format = (
                            logger_config.get("formatters").get(k).get("format")
                        )
                        logger_config["formatters"][k]["format"] = (
                            "%(color)s" + current_format + "%(reset)s"
                        )

            config.dictConfig(logger_config)
        if os.name == 'nt': 
            os.system("cls" or "clear")  # for windows support
    except:
        pass

    return logger
