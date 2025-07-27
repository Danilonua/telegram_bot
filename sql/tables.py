from sql.connect import sql_conn


connect_info = sql_conn.conn()
connect, cursor = connect_info


class Tables:
    def __init__(self, chat_id, user_id, username):
        self.chat_id = chat_id
        self.user_id = user_id
        self.username = username
        self.level = 0
        self.local_spammer = 0
        self.global_spammer = 0
        self.pydollar = 0
        self.warns = 0
        self.lockdown_status = 0
        self.mats_status = 0
        self.check_sticker = 0
        self.baned = 0
        self.muted = 0
        self.promo_status = 0
        self.spam_status = 0

    def users_db(self, chat_id, user_id, username, level=0, local_spammer=0, global_spammer=0, pydollar=0, warns=0,
                 baned=0, muted=0, promo_status=0):
        """Функция получает id, уровень пользователя, id чата, спамер ли он, его имя и
         вставляет эту информацию о пользователе в базу данных"""

        self.chat_id = chat_id
        self.user_id = user_id
        self.username = username
        self.level = level
        self.local_spammer = local_spammer
        self.global_spammer = global_spammer
        self.pydollar = pydollar
        self.warns = warns
        self.baned = baned
        self.muted = muted
        self.promo_status = promo_status

        cursor.execute("""CREATE TABLE IF NOT EXISTS user(
            user_id INTEGER,
            level INTEGER,
            chat_id BIGINT,
            local_spammer TEXT,
            global_spammer TEXT,
            username TEXT,
            pydollar INTEGER,
            warn INTEGER,
            baned TEXT,
            muted TEXT,
            promo_status TEXT
        )
        """)

        connect.commit()

        users_list = [self.user_id, self.level, self.chat_id, self.local_spammer, self.global_spammer, self.username,
                      self.pydollar, self.warns, self.baned, self.muted, self.promo_status]
        cursor.execute("INSERT INTO user VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", users_list)

        connect.commit()

    def chat_db(self, chat_id, lockdown_status=0, mats_status=0, spam_status=0, check_sticker=0):
        """Функция получает id, уровень пользователя, id чата, спамер ли он, его имя и
         вставляет эту информацию о пользователе в базу данных"""

        self.chat_id = chat_id
        self.lockdown_status = lockdown_status
        self.mats_status = mats_status
        self.check_sticker = check_sticker
        self.spam_status = spam_status

        cursor.execute("""CREATE TABLE IF NOT EXISTS chat(
            chat_id BIGINT,
            lockdown_status TEXT,
            mats_status TEXT,
            spam_status TEXT,
            check_sticker TEXT
        )
        """)

        connect.commit()

        users_list = [self.chat_id, self.lockdown_status, self.mats_status, self.spam_status, self.check_sticker]
        cursor.execute("INSERT INTO chat VALUES(%s,%s,%s,%s,%s);", users_list)

        connect.commit()
