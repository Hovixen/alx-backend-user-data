#!/usr/bin/env python3
""" Regex-in function """
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ function returns log message obfuscated """
    msg = re.sub("({})=[^{}]+".format("|".join(fields), separator),
                 lambda r: "{}={}".format(r.group(1), redaction), message)
    return msg
