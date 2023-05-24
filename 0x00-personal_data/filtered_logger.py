#!/usr/bin/env python3
"""Log message obfuscating module"""

import re
from typing import List
import logging


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
    for fld in fields:
        message = re.sub(r"{}=[^{}]*{}".format(fld, separator, separator),
                         "{}={}{}".format(fld, redaction, separator), message)
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
