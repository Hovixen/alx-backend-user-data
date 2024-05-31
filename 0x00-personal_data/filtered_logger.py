#!/usr/bin/env python3
""" Regex-in function """
import re
from typing import List, Tuple
import logging

PII_FIELDS: Tuple[str] = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ function returns log message obfuscated """
    msg = re.sub("({})=[^{}]+".format("|".join(fields), separator),
                 lambda r: "{}={}".format(r.group(1), redaction), message)
    return msg


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        self.fields = fields

        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ function formats the log message """
        msg = super(RedactingFormatter, self).format(record)
        f_msg = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return f_msg


def get_logger() -> logging.Logger:
    """ function returns a logging.Logger """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logger.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII))
    logger.addHandler(stream_handler)

    return logger
