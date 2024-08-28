#!/usr/bin/env python3
"""Module for personal data project
"""

import logging
import os
import mysql.connector
import re
from typing import List

patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}
# Tuple of PII fields
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class

    Update the class to accept a list of strings fields constructor argument.
    Implement the format method to filter values in incoming log records using
    filter_datum. Values for fields in fields should be filtered.
    DO NOT extrapolate FORMAT manually. The format method should be less than
    5 lines long.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializes the class.

        Args:
            fields (List[str]): The fields.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records using filter_datum.

        Args:
            record (logging.LogRecord): A logging.LogRecord instance.

        Returns:
            str: A string with all occurrences of the `self.fields` in
            `record.message` replaced by the `self.REDACTION` string.
        """
        msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
) -> str:
    """Returns the log message with certain fields obfuscated.

    Args:
        fields (List[str]): a list of strings representing all fields to
        obfuscate.
        redaction (str): a string representing by what the field will be
        obfuscated.
        message (str): a string representing the log line.
        separator (str): a string representing by which character is separating
        all fields in the log line (message).

    Returns:
        str: the log message obfuscated.
    """
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object named "user_data".

    The logger should be named "user_data" and only log up to logging.INFO
    level.
    It should not propagate messages to other loggers. It should have a
    StreamHandler with RedactingFormatter as formatter.

    Returns:
        logging.Logger: A logging.Logger instance.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    logger.propagate = False
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database
    (mysql.connector.connection.MySQLConnection object).

    Connects to a secure database using credentials from environment variables.

    Returns:
        mysql.connector.connection.MySQLConnection: Connector to the
        database.
    """
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return connection


def main() -> None:
    """Obtain a database connection using get_db and retrieve all rows in
    the users table and display each row under a filtered format.
    """
    logger = get_logger()

    db = get_db()
    cursor = db.cursor()

    # Retrieve all rows in the users table
    cursor.execute("SELECT * FROM users")
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    # Display each row under a filtered format
    for row in rows:
        message = "; ".join([f"{columns[i]}={row[i]}"
            for i in range(len(columns))])
        logger.info(filter_datum(PII_FIELDS, RedactingFormatter.REDACTION,
                                 message, RedactingFormatter.SEPARATOR))

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
