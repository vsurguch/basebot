import sqlite3
import unittest
from os import path

from .. import config
from ..src.dbutils import SqliteConnect, getRow, Selection
from ..src.sql_comapision_enum import Comparision


class TestDB(unittest.TestCase):

    dbname = path.join(config.INSTANCE, "data/test.sqlite")
    scriptname = path.join(config.INSTANCE, "data/sql.script")

    # def __init__(self, methodName):
    #     super(TestDB, self).__init__(methodName)

    # @classmethod
    # def setUpClass(cls):
    #     conn = sqlite3.connect(cls.dbname, detect_types=sqlite3.PARSE_DECLTYPES)


    def setUp(self):
        self.conn = sqlite3.connect(self.dbname, detect_types=sqlite3.PARSE_DECLTYPES)
        with open(self.scriptname, 'r', encoding='utf-8') as f:
            script = '\n'.join(f.readlines())
            self.conn.executescript(script)
        # sql = "INSERT INTO person (name,age, id_address) VALUES ('Ivan',10, 1), ('Petr', 21, 2);"
        # self.conn.execute(sql)
        self.conn.commit()


    def tearDown(self):
        self.conn.close()


    def test_SqliteConnectCreate(self):
        connection = SqliteConnect(self.dbname)
        RowClass = getRow("business", ["name", "phone"])
        connection.create_table(RowClass, name='TEXT', phone='TEXT')
        try:
            sql = "INSERT INTO business (name, phone) VALUES ('Beeline', '+79035550000')"
            self.conn.execute(sql)
            sql = f"SELECT * FROM business"
            rows = self.conn.execute(sql).fetchall()
            self.assertEqual(len(rows), 1)
        except sqlite3.OperationalError as e:
            self.fail(str(e))


    def test_SqliteConnectGet(self):
        connection = SqliteConnect(self.dbname)
        RowClass = getRow("person", ["name", "age", "id_address"])
        rows = connection.get(RowClass)

        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0].name, 'Petr')
        self.assertEqual(rows[0].age, 10)
        self.assertEqual(rows[1].name, 'Ivan')
        self.assertEqual(rows[1].age, 21)
        self.assertEqual(rows[2].name, 'Anna')
        self.assertEqual(rows[2].age, 29)


    def test_SqliteConnectGetLimit(self):
        connection = SqliteConnect(self.dbname)
        RowClass = getRow("person", ["name", "age", "id_address"])
        rows = connection.get(RowClass, 1)

        self.assertEqual(len(rows), 1)


    def test_SqliteConnectPut(self):
        connection = SqliteConnect(self.dbname)
        RowClass = getRow("person", ["name", "age", "id_address"])
        row = RowClass(name='John', age=30, id_address=1)
        connection.put(row)

        sql = "SELECT * FROM person"
        rows = self.conn.execute(sql).fetchall()
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[-1][1], 'John')


    def test_SqliteConnectDelete(self):
        connection = SqliteConnect(self.dbname)
        RowClass = getRow("person", ["name", "age", "id_address"])
        rows = connection.get(RowClass)

        connection.delete(rows[0])
        sql = "SELECT * FROM person"
        rows = self.conn.execute(sql).fetchall()
        self.assertEqual(len(rows), 2)


    def test_SqliteConnectModify(self):
        connection = SqliteConnect(self.dbname)
        RowClass = getRow("person", ["name", "age", "id_address"])
        rows = connection.get(RowClass, name='Ivan')
        modified = connection.modify(rows[0], name='Sergei')
        rows = connection.get(RowClass, name='Sergei')
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].name, 'Sergei')
        self.assertEqual(modified.name, 'Sergei')

    # def test_Selection(self):
    #     RowClassL = getRow("person", ["name", "age", "id_address"])
    #     RowClassR = getRow("address", ["city", "street", "n"])
    #     selection = Selection(RowClassL).join(RowClassR, "id_address")
    #     print(selection.sql)
    #     self.assertEqual(1, 1)

    def test_SelectionSelect(self):
        RowClassL = getRow("person", ["name", "age", "id_address"])
        RowClassR = getRow("address", ["city", "street", "n"])
        selection = Selection(RowClassL).join(RowClassR, "id_address")
        connection = SqliteConnect(self.dbname)
        result = connection.get_joined(selection)
        self.assertEqual(len(result), 3)


    def test_Order(self):
        connection = SqliteConnect(self.dbname)
        RowClass = getRow("person", ["name", "age", "id_address"])
        rows = connection.get(RowClass, _limit=1, _order='name, age')
        self.assertEqual('Anna', rows[0].name)


    def test_Order_age(self):
        connection = SqliteConnect(self.dbname)
        RowClass = getRow("person", ["name", "age", "id_address"])
        rows = connection.get(RowClass, _limit=1, _order='age')
        self.assertEqual('Petr', rows[0].name)


    def test_Comparision(self):
        connection = SqliteConnect(self.dbname)
        RowClass = getRow("person", ["name", "age", "id_address"])
        rows = connection.get(RowClass, age=(Comparision.More, 16))
        self.assertEqual(2, len(rows))


    def test_Comparision_Ordeer(self):
        connection = SqliteConnect(self.dbname)
        RowClass = getRow("person", ["name", "age", "id_address"])
        rows = connection.get(RowClass, _limit=1, _order='name', age=(Comparision.More, 16))
        self.assertEqual(1, len(rows))
        self.assertEqual('Anna', rows[0].name)


