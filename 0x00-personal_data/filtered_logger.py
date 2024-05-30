#!/usr/bin/env python3
""" Regex-in function """
import re
from typing import List
import logging


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

    def __init__(self, fields: List[str]):
        self.fields = fields

        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ function formats the log message """
        msg = super(RedactingFormatter, self).format(record)
        f_msg = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return f_msg
