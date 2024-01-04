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
        self.database_octane = pymysql.connect(
            host="n2.proxied.host",
            port=3306,
            user="u104_tgIeTOHavN",
            password="XAGt@5j3^R9l^V56lAvShWPt",
            database="s104_OctaneDB",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )

    def ping_db(self):
        return self.database.ping()

    def ping_octane_db(self):
        return self.database_octane.ping()

    def kermit(self):
        self.database.close()
        self.database_octane.close()
