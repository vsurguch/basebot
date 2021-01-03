from os import path

from src.dbutils import SqliteConnect, getRow


def create_table(db_filename):
    connection = SqliteConnect(db_filename)
    RowClass = getRow('reminder',
                      ['chat_id', 'date', 'time', 'text', 'important'])

    connection.create_table(RowClass,
                            chat_id='INTEGER',
                            date='INTEGER',
                            time='INTEGER',
                            text='TEXT',
                            complete='BOOLEAN',
                            important='BOOLEAN')


def show_table(db_filename):
    connection = SqliteConnect(db_filename)
    RowClass = getRow('reminder',
                      ['chat_id', 'date', 'time', 'text', 'important'])
    rows = connection.get(RowClass)
    for row in rows:
        print(row)


def main():
    db_filename = 'data/reminder.sqlite'
    db_path = path.join(path.dirname(__file__),
                        db_filename)
    # create_table(db_path)
    show_table(db_path)


if __name__ == '__main__':
    main()