from os import path

from ..config import INSTANCE
from .dbutils import SqliteConnect, getRow
from .parse_utils import convertDateStr, convertTimeStr


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


def dbmain_termin(create=True, verbose=True, *args):

    db_filename = 'data/termin.sqlite'
    RowClass = getRow("termin", ['chat_id', 'name', 'date', 'time', 'phone', 'text', 'complete'])
    kwargs = {'chat_id': 'INTEGER',
                'name': 'TEXT',
                'date': 'INTEGER',
                'time': 'INTEGER',
                'phone': 'INTEGER',
                'text': 'TEXT',
              'complete': 'BOOLEAN'
              }

    main(db_filename, RowClass, kwargs, create, verbose)


def dbmain_nextplease(create=True, verbose=True, *args):

    db_filename = 'data/nextplease.sqlite'
    RowClass = getRow('appointments',
                      ['chat_id', 'name', 'phone', 'date', 'time', 'complete'])
    kwargs = {'chat_id': 'INTEGER',
              'name': 'TEXT',
              'phone': 'INTEGER',
              'date': 'INTEGER',
              'time': 'INTEGER',
              'complete': 'BOOLEAN'
              }

    main(db_filename, RowClass, kwargs, create, verbose)


def dbmain_reminder(create=True, verbose=True, *args):

    db_filename = 'data/remind.sqlite'
    RowClass = getRow('reminder',
                      ['chat_id', 'date', 'time', 'text', 'important'])
    kwargs = {'chat_id': 'INTEGER',
              'date': 'INTEGER',
              'time': 'INTEGER',
              'text': 'TEXT',
              'important': 'BOOLEAN'
              }
    main(db_filename, RowClass, kwargs, create, verbose)


def dbmain_slots(create=True, verbose=True, *args):
    db_filename = 'data/nextplease.sqlite'
    RowClass = getRow('slots',
                      ['date', 'time', 'free'])
    kwargs = {
              'date': 'INTEGER',
              'time': 'INTEGER',
            'free': 'BOOLEAN',
              }

    main(db_filename, RowClass, kwargs, create, verbose)


def main(db_filename, RowClass, kwargs, create=True, verbose=True):

    db_path = path.join(INSTANCE, db_filename)
    if create:
        create_table(db_path, RowClass, kwargs)
    if verbose:
        show_table(db_path, RowClass)


def dbslots_addslotsrange(conn, RowClass, datestr, starttimestr, endtimestr, duration=30):

    starttime = convertTimeStr(starttimestr)
    endtime = convertTimeStr(endtimestr)
    n_slots = int(endtime - starttime) // (duration * 60)
    for i in range (n_slots):
        row = RowClass(date=convertDateStr(datestr), time=starttime + i * duration * 60, free=True)
        conn.put(row)


def dbslots_fill(create, verbose, datestr, starttimestr, endtimestr):
    db_filename = 'data/nextplease.sqlite'
    db_path = path.join(INSTANCE, db_filename)
    RowClass = getRow('slots',
                      ['date', 'time', 'free'])
    conn = SqliteConnect(db_path)
    try:
        dbslots_addslotsrange(conn, RowClass, datestr, starttimestr, endtimestr)
    except Exception as e:
        print(str(e))

