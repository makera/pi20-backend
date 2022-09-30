import sqlite3

_connection = None


def get_connection():
    global _connection
    if _connection is None:
        _connection = sqlite3.connect("base.sqlite")
    return _connection
