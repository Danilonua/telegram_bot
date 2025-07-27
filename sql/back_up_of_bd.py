from sql.tables import Tables
from sql.search import Search
from sql.update import Update
from sql.connect import sql_conn


connect_info = sql_conn.conn()
connect, cursor = connect_info


class BD:
    def __init__(self, chat_id, user_id, username):
        self.chat_id = chat_id
        self.user_id = user_id
        self.username = username
        self.level = 0
        self.spammer = 0
        self.pydollar = 0
        self.warns = 0
        self.lockdown_status = 0
        self.mats_status = 0
        self.check_sticker = 0
        self.spam_status = 0
        self.search = Search(self.user_id, self.chat_id, self.username)
        self.update = Update(self.user_id, self.chat_id, self.username)
        self.tables = Tables(self.user_id, self.chat_id, self.username)

    def warn_db(self, chat_id, user_id):

        self.chat_id = chat_id
        self.user_id = user_id

        is_person_heir = db.search.search_person_in_user(self.chat_id, self.user_id)
        if is_person_heir is None:
            self.warns = 1
            db.tables.users_db(self.chat_id, self.user_id, None, warns=self.warns)
        else:
            is_person_warns = db.search.search_warns(self.chat_id, self.user_id)
            if is_person_warns is None:
                self.warns = 1
                db.update.update_warns(self.warns, self.chat_id, self.user_id)
            else:
                how_many_warns = str(db.search.search_warns(self.chat_id, self.user_id))
                self.warns = int(how_many_warns) + 1
                db.update.update_warns(self.warns, self.chat_id, self.user_id)
                return self.warns

    def un_warn_db(self, chat_id, user_id):

        self.chat_id = chat_id
        self.user_id = user_id

        is_person_heir = db.search.search_person_in_user(self.chat_id, self.user_id)
        if is_person_heir is None:
            db.tables.users_db(self.chat_id, self.user_id, None)
        else:
            is_person_warns = db.search.search_warns(self.chat_id, self.user_id)
            if is_person_warns is None:
                return None
            else:
                how_many_warns = str(db.search.search_warns(self.chat_id, self.user_id)[0])
                self.warns = int(how_many_warns)
                self.warns -= 1
                db.update.update_warns(self.warns, self.chat_id, self.user_id)
                return self.warns

    def all_admins(self, chat_id):
        global cursor

        """Функция ищет всех администраторов в группе"""

        self.chat_id = chat_id

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT username, level FROM user WHERE chat_id = {self.chat_id} AND level > 0 AND level < 5")
        all_admins = cursor.fetchall()
        return all_admins

    def all_admins_id(self, chat_id):
        global cursor

        """Функция ищет id администраторов в группе."""

        self.chat_id = chat_id

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT user_id FROM user WHERE chat_id = {self.chat_id} AND level > 0 AND level < 5")
        all_admins = cursor.fetchall()
        return all_admins


db = BD(0, 0, None)
