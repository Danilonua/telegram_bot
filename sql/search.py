from sql.connect import sql_conn


connect_info = sql_conn.conn()
connect, cursor = connect_info


class Search:
    def __init__(self, user_id, chat_id, username):
        self.user_id = user_id
        self.chat_id = chat_id
        self.username = username

    def search_person_in_chat(self, chat_id):
        global cursor

        """Функция проверяет, есть ли пользователь в базе данных, если его нет, система возвращает None,
        а если есть, то возвращает всю информацию про него"""

        self.chat_id = chat_id

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT * FROM chat WHERE chat_id={self.chat_id}")
        is_person_heir = cursor.fetchone()
        return is_person_heir

    def search_person_in_user(self, chat_id, user_id):
        global cursor

        """Функция проверяет, есть ли пользователь в базе данных, если его нет, система возвращает None,
        а если есть, то возвращает всю информацию про него"""

        self.chat_id = chat_id
        self.user_id = user_id

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT * FROM user WHERE user_id={self.user_id} AND chat_id={self.chat_id}")
        is_person_heir = cursor.fetchone()
        return is_person_heir

    def search_level(self, chat_id, user_id):
        global cursor

        """Функция ищет level пользователя в базе данных и возвращает результат """

        self.chat_id = chat_id
        self.user_id = user_id

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT level FROM user WHERE user_id = {self.user_id} AND chat_id = {self.chat_id}")
        result = cursor.fetchone()
        return result

    def search_lockdown(self, chat_id):
        global cursor

        """Функция ищет lockdown_status в базе данных и возвращает результат """

        self.chat_id = chat_id

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT lockdown_status FROM chat WHERE chat_id ='{self.chat_id}'")
        result = cursor.fetchone()
        return result

    def search_check_sticker(self, chat_id):
        global cursor

        """Функция ищет lockdown_status в базе данных и возвращает результат """

        self.chat_id = chat_id

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT check_sticker FROM chat WHERE chat_id ='{self.chat_id}'")
        result = cursor.fetchone()
        return result

    def search_mats(self, chat_id):
        global cursor

        """Функция ищет lockdown_status в базе данных и возвращает результат """

        self.chat_id = chat_id

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT mats_status FROM chat WHERE chat_id = {self.chat_id}")
        result = cursor.fetchone()
        return result

    def search_spam(self, chat_id):
        global cursor

        """Функция ищет spam_status в базе данных и возвращает результат """

        self.chat_id = chat_id

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT spam_status FROM chat WHERE chat_id = {self.chat_id}")
        result = cursor.fetchone()
        return result

    def search_warns(self, chat_id, user_id):
        global cursor

        self.chat_id = chat_id
        self.user_id = user_id

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT warn FROM user WHERE user_id = {self.user_id} AND chat_id = {self.chat_id}")
        result = cursor.fetchone()
        if result is None:
            return 1
        result = str(result)[1:][:len(result) - 3]
        return result

    def search_id(self, chat_id, username):
        global cursor

        """ Функция принимает имя пользователя и id чата и возвращает id пользователя"""

        self.chat_id = chat_id
        self.username = username

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT user_id FROM user WHERE username = '{self.username}' AND chat_id = '{self.chat_id}'")
        result = cursor.fetchone()
        return result

    def search_promo(self, user_id):
        global cursor

        """ Функция принимает имя пользователя и id чата и возвращает id пользователя"""

        self.user_id = user_id

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT promo_status FROM user WHERE user_id = '{self.user_id}'")
        result = cursor.fetchone()
        return result

    def search_username(self, chat_id, user_id):
        global cursor

        """ Функция принимает имя пользователя и id чата и возвращает id пользователя"""

        self.chat_id = chat_id
        self.user_id = user_id

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT username FROM user WHERE user_id = '{self.user_id}' AND chat_id = '{self.chat_id}'")
        result = cursor.fetchone()
        return result

    def search_local_spammer(self, chat_id, user_id):
        global cursor

        """Функция ищет пользователя и берет с базы данных local_spammer"""

        self.chat_id = chat_id
        self.user_id = user_id

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT local_spammer FROM user WHERE user_id = {self.user_id} AND chat_id = {self.chat_id}")
        check_local_spammer = cursor.fetchone()
        return check_local_spammer

    def search_global_spammer(self, user_id):
        global cursor

        """Функция ищет пользователя и берет с базы данных local_spammer"""

        self.user_id = user_id

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT global_spammer FROM user WHERE user_id = {self.user_id}")
        check_global_spammer = cursor.fetchone()
        return check_global_spammer

    def search_pydollar(self, user_id):
        global cursor

        """ Функция ищет пользователя и берет с базы данных pydollar"""

        self.user_id = user_id

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT pydollar FROM user WHERE user_id={self.user_id}")
        result = cursor.fetchone()
        return result

    @staticmethod
    def search_max_pydollar():
        global cursor

        """ Функция ищет пользователя и берет с базы данных pydollar"""

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT username, user_id, pydollar FROM user")
        result = cursor.fetchall()
        original_list = [list(t) for t in result]
        filtered_list = [lst for lst in original_list if lst[2] != 0]
        sorted_list = sorted(filtered_list, key=lambda x: x[2], reverse=True)
        final_list = sorted_list[:10]
        return final_list

    def search_ban(self, chat_id, user_id):
        global cursor

        """Функция ищет baned в базе данных и возвращает результат"""

        cursor = sql_conn.reconnect()
        self.chat_id = chat_id
        self.user_id = user_id

        cursor.execute(f"SELECT baned FROM user WHERE user_id = {self.user_id} AND chat_id = {self.chat_id}")
        result = cursor.fetchone()
        result = str(result)[1:][:len(result) - 3]
        return result

    def search_mute(self, chat_id):
        global cursor

        """Функция ищет muted в базе данных и возвращает результат"""

        self.chat_id = chat_id

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT muted FROM user WHERE chat_id = {self.chat_id}")
        result = cursor.fetchone()
        result = str(result)[1:][:len(result) - 3]
        return result

    def search_banned_person(self, chat_id):
        global cursor

        self.chat_id = chat_id

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT username, user_id FROM user WHERE chat_id = {self.chat_id} AND baned = 1")
        result = cursor.fetchone()
        return result

    def search_muted_person(self, chat_id):
        global cursor

        self.chat_id = chat_id

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT username, user_id FROM user WHERE chat_id = {self.chat_id} AND muted = 1")
        result = cursor.fetchone()
        return result

    def search_warned_person(self, chat_id):
        global cursor

        self.chat_id = chat_id

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT username, user_id, warn FROM user WHERE chat_id = {self.chat_id} AND warn != 0")
        result = cursor.fetchone()
        return result

    def unban_all(self, chat_id):
        global cursor

        self.chat_id = chat_id

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT user_id FROM user WHERE chat_id = {self.chat_id} AND baned = 1")
        result = cursor.fetchone()
        return result

    def unmute_all(self, chat_id):
        global cursor

        self.chat_id = chat_id

        cursor = sql_conn.reconnect()
        cursor.execute(f"SELECT user_id FROM user WHERE chat_id = {self.chat_id} AND muted != 0")
        result = cursor.fetchone()
        return result
