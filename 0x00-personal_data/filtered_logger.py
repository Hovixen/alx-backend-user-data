#!/usr/bin/env python3
""" Regex-in function """
import re
import os
import mysql.connector
from mysql.connector import connection
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

    def __init__(self, fields: List[str]):
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

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """ function connects to the database """
    db_host = os.getenv("PERSONAL_DATA_DB_HOST")
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD")
    db_database = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
            host=db_host,
            user=db_username,
            password=db_password,
            database=db_database
    )


def main():
    """
    main entry point
    """
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names
    for row in cursor:
        message = "".join("{}={}; ".format(k, v) for k, v in zip(fields, row))
        logger.info(message.strip())
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
