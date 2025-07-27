import pymysql


class Sql_connect():
    def conn(self):
        """Функция подключается к базе данных"""

        global connect
        global cursor
        host = 'database.c8c16aojfy27.us-east-1.rds.amazonaws.com'
        port = 3306
        database = 'pydollars'
        user = 'danya'
        password = 'e3dDiUV2dY8582E'

        connect = pymysql.connect(host=host, port=port, db=database, user=user, passwd=password)

        cursor = connect.cursor()
        return connect, cursor

    def reconnect(self):
        """Функция обновляет подключение к базе данных, для получения новой информации"""

        sql_conn = Sql_connect()
        connect.close()
        sql_conn.conn()
        return cursor


sql_conn = Sql_connect()
