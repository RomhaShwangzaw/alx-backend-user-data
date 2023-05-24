#!/usr/bin/env python3
"""Log message obfuscating module"""

import re
from typing import List


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
        message = re.sub(r"{}=[\w/]*{}".format(field, separator), "{}={}{}".
                         format(field, redaction, separator), message)
    return message
