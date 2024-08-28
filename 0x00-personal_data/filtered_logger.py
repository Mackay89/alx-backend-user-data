#!/usr/bin/env python3
"""
This module provides a function to obfuscate sensitive
information in log messages.
"""

import re
from typing import List


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Replaces field values in a log message with a redaction string.

    Args:
        fields (List[str]): The list of fields to be obfuscated.
        redaction (str): The string to replace the field values with.
        message (str): The log message containing
        the fields.
        separator (str): The character separating the fields
        in the log message.

    Returns:
        str: The obfuscated log message.
    """
    pattern = '|'.join([
        f'{field}=[^{separator}]*' for field in fields
    ])
    return re.sub(
        pattern,
        lambda m: m.group(0).split('=')[0] + '=' + redaction,
        message
    )
