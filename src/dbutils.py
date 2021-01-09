from collections import namedtuple
import sqlite3
from .sql_comapision_enum import Comparision


class Row():
    pass


def getRow(name, fields, defaults=None, add_id=True):
    defaults = (None,) * len(fields) if defaults is None else defaults
    if add_id:
        fields = ['id',] + fields
        defaults = (0,) + defaults
    row = namedtuple(name, fields)
    row.__new__.__defaults__ = defaults
    return row


class Selection:

    # maybe add dict with all created RowClasses to facilitate corresponding Class retrieval

    def __init__(self, RowClass):
        name = RowClass.__name__
        self.fields = [f"{name}.{field}" for field in RowClass._fields]
        self.field_names = [f"{name}_{field}" for field in RowClass._fields]
        self.sql_ = f" FROM {name} AS {name}"
        self.tables = [name, ]
        self.RowClass = None

    def join(self, RightRowClass, left, jtype='left', right='id', LeftRowClass=None):
        name = RightRowClass.__name__
        name_left = LeftRowClass.__name__ if LeftRowClass is not None else self.tables[-1]
        self.fields += [f"{name}.{field}" for field in RightRowClass._fields]
        self.field_names += [f"{name}_{field}" for field in RightRowClass._fields]
        self.sql_ += f" {jtype.upper()} JOIN {name} AS {name} ON {name_left}.{left}={name}.{right}"
        self.tables.append(name)
        return self

    def getRowClass(self):
        if self.RowClass is None:
            self.RowClass = getRow('Joined' + ''.join(self.tables), self.field_names, add_id=False)
        return self.RowClass

    @property
    def sql(self):
        return f"SELECT {','.join(self.fields)}" + self.sql_


class SqliteConnect():
    dbname = ''
    instance = None

    # def relate(self, RowLeft, RowRight, left, right):
    #     sql = f"ALTER TABLE {RowLeft.__name__} ADD FOREGIN KEY ({left}) REFERENCES {RowRight.__name__}({right})"
    #     conn = self.get_conn()
    #     conn.execute(sql)
    #     conn.close()

    def __new__(cls, dbname):
        cls.dbname = dbname
        if cls.instance is None:
            cls.instance = super(SqliteConnect, cls).__new__(cls)
        return cls.instance

    def _get_conn(self):
        return sqlite3.connect(self.dbname, detect_types=sqlite3.PARSE_DECLTYPES)

    def _execute(self, sql, values=None, commit=False):
        conn = self._get_conn()
        conn.cursor().execute(sql, values)
        if commit:
            conn.commit()
        conn.close()

    def _get_generic(self, RowClass, sql_base, _limit=None, _offset=None, _order=None, **kwargs):
        limit = f"LIMIT {_limit}" if _limit is not None else ''
        offset = f"OFFSET {_offset}" if _offset is not None else ''
        order = f"ORDER BY {_order}" if _order is not None else ''

        # condition = ' AND '.join([f'{item}=?' for item in kwargs.keys()])
        # condition_values = [val for val in kwargs.values()] if condition else []
        condition = ''
        condition_values = []
        for field, value in kwargs.items():
            comp = Comparision.Equal.value
            logical = 'AND'
            if isinstance(value, tuple):
                comp = value[0].value
                condition_values.append(value[1])
            else:
                condition_values.append(value)
            condition += f' {logical} ' + f'{field}{comp}?'

        condition = f"WHERE {condition[5:]}" if condition else ''
        sql = f"{sql_base} {condition} {order} {limit} {offset}"
        conn = self._get_conn()
        cur = conn.cursor()
        rows = [RowClass._make(row) for row in cur.execute(sql, condition_values).fetchall()]
        conn.close()
        return rows

    def create_table(self, RowClass, drop_if_exists=True, foreign_keys_=None, **kwargs):
        kwargs['id'] = 'INTEGER PRIMARY KEY AUTOINCREMENT'
        fields = ','.join([f"{name} {kwargs[name]}" for name in RowClass._fields])
        foreign_keys = ', '.join([f'FOREIGN KEY ({item[0]}) REFERENCES {item[1]}' for item in foreign_keys_]) \
            if foreign_keys_ is not None else ''

        sql = f"CREATE TABLE {RowClass.__name__} ({fields} {foreign_keys})"

        if drop_if_exists:
            sql = f"DROP TABLE IF EXISTS {RowClass.__name__};\n" + sql

        conn = self._get_conn()
        conn.executescript(sql)
        conn.close()

    def get(self, RowClass, _limit=None, _offset=None, _order=None, **kwargs):
        sql_base = f"SELECT * FROM {RowClass.__name__}"
        return self._get_generic(RowClass, sql_base, _limit, _offset, _order, **kwargs)

    def get_joined(self, selection, _limit=None, _offset=None, **kwargs):
        RowClass = selection.getRowClass()
        return self._get_generic(RowClass, selection.sql, _limit, _offset, **kwargs)

    def put(self, row):
        fields = row._fields
        values = [val for val in row]
        sql = f"INSERT INTO {type(row).__name__} ({','.join(fields[1:])}) VALUES ({','.join(['?',]*(len(values)-1))})"
        self._execute(sql, values[1:], commit=True)

    def delete(self, row):
        sql = f"DELETE FROM {type(row).__name__} WHERE id=?"
        self._execute(sql, (row.id,), commit=True)

    def modify(self, row, **kwargs):
        sql = f"UPDATE {type(row).__name__} SET {','.join([f'{field}=?'for field in kwargs.keys()])} WHERE id=?"
        values = [val for val in kwargs.values()] + [row.id,]
        self._execute(sql, values, commit=True)
        return row._replace(**kwargs)


# class TabController:
#     __slots__ = []
#     def print(self):
#         print(str(self._fields))
#         return
#
#
# def nt_factory(name, fields, defaults=None):
#     nt = namedtuple(name, fields)
#     nt.__new__.__defaults__ = (None,) * len(fields) if defaults is None else defaults
#
#     class Tab(nt, TabController):
#         pass
#
#     return nt


def main():
    RowClass = getRow('Test', ['name', 'age'], ("Joan", 18))
    item = RowClass(name = "Ivan", age = 20)
    item2 = RowClass()
    print(item._fields, item._asdict().values(), item.__sizeof__())
    print(item2)


if __name__ == '__main__':
    main()