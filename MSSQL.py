from telebot import types
import pyodbc
from config import *


class MSSQL:
    def __init__(self):
        self.connection = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=" + SERVER + ";"
            "DATABASE=" + DATABASE + ";"
            "UID=" + UID_DB + ";"
            "PWD=" + PSWD_DB + ";"
        )

    def execute(self, sql, params=None):
        cursor = self.connection.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        cursor.commit()

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results

    def execute_non_query(self, query, params=None):
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        cursor.commit()
        cursor.close()

    def disconnect(self):
        self.connection.close()
