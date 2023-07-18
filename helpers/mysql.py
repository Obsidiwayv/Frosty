import pymysql.cursors


class MySQLHelper:
    def __init__(self):
        self.database = pymysql.connect(
            host="n2.proxied.host",
            port=3306,
            user="u104_RR7zdEid47",
            password="o!q8q8kNMRL.!qCUuoU^MRdH",
            database="s104_WSQL",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )

    def ping_db(self):
        return self.database.ping()

    def kermit(self):
        self.database.close()
