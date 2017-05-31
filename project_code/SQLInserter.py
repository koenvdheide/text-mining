from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


class SQLInserter:
    # "mysql+mysqlconnector://root:usbw@localhost:3307/test"

    def __init__(self, sqldialect="mysql", driver="mysqlconnector", username="root", password="usbw", host="localhost",
                 port="3307", database="test"):
        engine_argument = sqldialect + "+" + driver + "://" + username + ":" + password + "@" + host + ":" + port + "/" + database
        self.engine = create_engine(engine_argument, echo=True)  # mogelijk text encoding nog toevoegen

        self.Base = automap_base()
        self.Base.prepare(self.engine, reflect=True)

    # Return list with table names
    def get_table_names(self):
        return list(self.Base.metadata.tables)

    # Return dictionary with table names as keys and column names as values
    def get_tables(self):
        return self.Base.metadata.tables

    # Return the table object containing the information of the specified table
    def get_table(self, tablename):
        return self.Base.metadata.tables[tablename]

    def insert_values(self, tablename, values, column_check=False):
        table_object = self.get_table(tablename)  # get table object belonging to the tablename

        if column_check == True and len(values) != len(table_object.columns):
            raise ColumnLengthMismatch("Amount of columns does not match amount of values to be inserted")

        else:
            ins = table_object.insert().values(values)
            self.__execute(ins)
            return ins

    def __execute(self, query):
        connection = self.engine.connect()
        connection.execute(query)


test = SQLInserter()
values = [14, None]  # NULL = None
test.insert_values('owo', values)


class ColumnLengthMismatch(Exception):
    pass
