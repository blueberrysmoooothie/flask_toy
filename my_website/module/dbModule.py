import pymysql
from settings import DB_HOST, DB_PORT, DB_ADMIN_ID, DB_ADMIN_PW, DB_NAME


class Database:
    def __init__(self):
        self.db = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_ADMIN_ID,
            passwd=DB_ADMIN_PW,
            db=DB_NAME,
            charset="utf8",
        )
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args={}):
        if "values" in args:
            self.cursor.executemany(query, args["values"])
        else:
            self.cursor.execute(query, args)

    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()
