from abc import ABC
from dataclasses import dataclass, fields, Field
from db import get_connection


def table_field_with_type(field: Field, primary_key):
    types_map = {
        int: 'INTEGER',
        float: 'REAL',
        str: 'TEXT',
        bytes: 'BLOB',
    }
    if field.name == primary_key:
        return '{} {} PRIMARY KEY AUTOINCREMENT'.format(field.name, types_map[field.type])
    return '{} {}'.format(field.name, types_map[field.type])


def clean_table_value(field: Field, value):
    if field.type == str:
        return "'{}'".format(value)
    return '{}'.format(value if value is not None else 'Null')


@dataclass
class BaseModel(ABC):
    id: int

    primary_key = 'id'

    @property
    def _table_name(self):
        return self.__class__.__name__.lower()

    @classmethod
    def _create_table(cls):
        sql = 'CREATE TABLE IF NOT EXISTS {} ({})'.format(
            cls.__name__.lower(),
            ', '.join(map(lambda f: table_field_with_type(f, cls.primary_key), fields(cls)))
        )
        cur = get_connection().cursor()
        cur.execute(sql)
        cur.close()

    def save(self):
        if not self.id:
            sql = 'INSERT INTO {} ({}) VALUES ({})'.format(
                self._table_name,
                ', '.join(map(lambda f: f.name, fields(self))),
                ', '.join(map(lambda f: clean_table_value(f, getattr(self, f.name)), fields(self)))
            )
        else:
            sql = 'UPDATE {} SET {} WHERE id={}'.format(
                self._table_name,
                ', '.join(map(lambda f: '{}={}'.format(f.name, clean_table_value(f, getattr(self, f.name))), fields(self))),
                self.id
            )
        cur = get_connection().cursor()
        cur.execute(sql)
        get_connection().commit()
        res = cur.execute('SELECT * FROM {} WHERE id={}'.format(self._table_name, cur.lastrowid)).fetchone()
        for col in range(len(fields(self))):
            setattr(self, fields(self)[col].name, res[col])
        cur.close()
        return self

    def delete(self):
        if self.id:
            sql = 'DELETE FROM {} WHERE id={}'.format(self._table_name, self.id)
            cur = get_connection().cursor()
            cur.execute(sql)
            get_connection().commit()
            cur.close()
        return self

    @classmethod
    def fetch_all(cls):
        sql = 'SELECT * FROM {}'.format(cls.__name__.lower())
        cur = get_connection().cursor()
        cur.execute(sql)
        items = [cls(*row) for row in cur.fetchall()]
        cur.close()
        return items
