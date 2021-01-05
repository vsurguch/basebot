from os import path

from ..config import INSTANCE
from .dbutils import SqliteConnect, getRow


# def create_table(db_filename):
#     connection = SqliteConnect(db_filename)
#     RowClass = getRow('reminder',
#                       ['chat_id', 'date', 'time', 'text', 'important'])
#
#     connection.create_table(RowClass,
#                             chat_id='INTEGER',
#                             date='INTEGER',
#                             time='INTEGER',
#                             text='TEXT',
#                             important='BOOLEAN')


def create_table(db_filename, RowClass, kwargs):
    connection = SqliteConnect(db_filename)
    connection.create_table(RowClass, **kwargs)


def show_table(db_filename, RowClass):
    connection = SqliteConnect(db_filename)
    rows = connection.get(RowClass)
    print(f'Rows in {db_filename}: {len(rows)}')
    for row in rows:
        print(row)


def main(create=True):
    # db_filename = 'data/termin.sqlite'
    # RowClass = getRow("termin", ['chat_id', 'name', 'date', 'time', 'phone', 'text', 'complete'])
    # kwargs = {'chat_id': 'INTEGER',
    #             'name': 'TEXT',
    #             'date': 'INTEGER',
    #             'time': 'INTEGER',
    #             'phone': 'INTEGER',
    #             'text': 'TEXT',
    #           'complete': 'BOOLEAN'
    #           }
    db_filename = 'data/remind.sqlite'
    RowClass = getRow('reminder',
                      ['chat_id', 'date', 'time', 'text', 'important'])
    kwargs = {'chat_id': 'INTEGER',
              'date': 'INTEGER',
              'time': 'INTEGER',
              'text': 'TEXT',
              'important': 'BOOLEAN'
              }
    db_path = path.join(INSTANCE, db_filename)
    if create:
        create_table(db_path, RowClass, kwargs)
    show_table(db_path, RowClass)


if __name__ == '__main__':
    main()