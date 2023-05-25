#!/usr/bin/env python3
"""Log message obfuscating module"""

import re
import os
import mysql.connector
from typing import List
import logging

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_logger() -> logging.Logger:
    """Creates a logger and returns it"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Creates a database connector and
    returns the connection object
    """
    mydb = mysql.connector.connect(
            host=os.environ.get('PERSONAL_DATA_DB_HOST'),
            user=os.environ.get('PERSONAL_DATA_DB_USERNAME'),
            password=os.environ.get('PERSONAL_DATA_DB_PASSWORD'),
            database=os.environ.get('PERSONAL_DATA_DB_NAME')
    )
    return mydb


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates log messages

    Args:
    `fields`   : a list of strings representing all fields to obfuscate
    `redaction`: a string representing by what the field will be obfuscated
    `message`  : a string representing the log line
    `separator`: a string representing by which character is separating
                 all fields in the log line (`message`)

    Return: The log message obfuscated
    """
    for field in fields:
        message = re.sub(r"{}=[^{}]*".format(field, separator),
                         "{}={}".format(field, redaction), message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats a log record"""
        msg = super(RedactingFormatter, self).format(record)
        txt = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt
