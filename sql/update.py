from sql.search import Search
from sql.tables import Tables
from sql.connect import sql_conn


connect_info = sql_conn.conn()
connect, cursor = connect_info


class Update:
    def __init__(self, user_id, chat_id, username):
        self.user_id = user_id
        self.chat_id = chat_id
        self.username = username
        self.level = 0
        self.search = Search(self.user_id, self.chat_id, self.username)
        self.tables = Tables(self.user_id, self.chat_id, self.username)

    def update_level(self, level, chat_id, user_id):

        self.chat_id = chat_id
        self.user_id = user_id
        self.level = level

        is_person_heir = self.search.search_person_in_user(self.chat_id, self.user_id)
        if is_person_heir is None:
            self.tables.users_db(self.chat_id, self.user_id, None, level=self.level)
        else:
            cursor.execute(
                f"UPDATE user SET level={self.level} WHERE user_id={self.user_id} AND"
                f" chat_id={self.chat_id}")
            connect.commit()

    def update_lockdown(self, lockdown_status, chat_id):

        self.chat_id = chat_id

        is_person_heir = self.search.search_person_in_chat(self.chat_id)
        if is_person_heir is None:
            update.tables.chat_db(self.chat_id, lockdown_status=lockdown_status)
        else:
            cursor.execute(f"UPDATE chat SET lockdown_status={lockdown_status} WHERE chat_id={self.chat_id}")
            connect.commit()

    def update_promo(self, promo_status, chat_id, user_id):

        self.chat_id = chat_id
        self.user_id = user_id

        is_person_heir = self.search.search_person_in_user(self.chat_id, self.user_id)
        if is_person_heir is None:
            update.tables.users_db(self.chat_id, self.user_id, None, promo_status=promo_status)
        else:
            cursor.execute(f"UPDATE user SET promo_status={promo_status} WHERE chat_id={self.chat_id}")
            connect.commit()

    def update_check_sticker(self, check_sticker, chat_id):

        self.chat_id = chat_id

        is_person_heir = update.search.search_person_in_chat(self.chat_id)
        if is_person_heir is None:
            update.tables.chat_db(self.chat_id, check_sticker=check_sticker)
        else:
            cursor.execute(f"UPDATE chat SET check_sticker={check_sticker} WHERE chat_id={self.chat_id}")
            connect.commit()

    def update_mats(self, mats_status, chat_id):

        self.chat_id = chat_id

        is_person_heir = update.search.search_person_in_chat(self.chat_id)
        if is_person_heir is None:
            update.tables.chat_db(self.chat_id, mats_status=mats_status)
        else:
            cursor.execute(f"UPDATE chat SET mats_status={mats_status} WHERE chat_id={self.chat_id}")
            connect.commit()
            return mats_status

    def update_username(self, chat_id, user_id, username):
        """Функция получает имя пользователя, его id и id чата, и если его там нет,
        заносит эту информацию в базу данных, а если он уже там есть, обновляет эту информацию"""

        self.chat_id = chat_id
        self.user_id = user_id
        self.username = username

        is_person_heir = update.search.search_person_in_user(self.chat_id, self.user_id)
        if is_person_heir is None:
            update.tables.users_db(self.chat_id, self.user_id, self.username)
        else:
            cursor.execute(f"UPDATE user SET username='{self.username}' WHERE user_id='{self.user_id}'"
                           f" AND chat_id='{self.chat_id}'"
                           f";")
            connect.commit()

    def update_local_spammer(self, local_spammer, chat_id, user_id):
        """Функция получает данные от search_person, если пользователь есть в базе данных,
         тогда изменяем local_spammer на 1, если пользователя нет, тогда добавляем его"""

        self.chat_id = chat_id
        self.user_id = user_id

        is_person_heir = update.search.search_person_in_user(self.chat_id, self.user_id)
        if is_person_heir is None:
            update.tables.users_db(self.chat_id, self.user_id, self.username, local_spammer=local_spammer)
        else:
            cursor.execute(f"UPDATE user SET local_spammer={local_spammer} WHERE user_id={self.user_id} AND"
                           f" chat_id={self.chat_id}")
            connect.commit()

    def update_global_spammer(self, global_spammer, chat_id, user_id):
        """Функция получает данные от search_person, если пользователь есть в базе данных,
         тогда изменяем global_spammer на 1, если пользователя нет, тогда добавляем его"""

        self.chat_id = chat_id
        self.user_id = user_id

        is_person_heir = update.search.search_person_in_user(self.chat_id, self.user_id)
        if is_person_heir is None:
            update.tables.users_db(self.chat_id, self.user_id, self.username, global_spammer=global_spammer)
        else:
            cursor.execute(f"UPDATE user SET global_spammer={global_spammer} WHERE user_id={self.user_id}")
            connect.commit()

    def update_warns(self, warns, chat_id, user_id):

        self.chat_id = chat_id
        self.user_id = user_id

        is_person_heir = update.search.search_person_in_user(self.chat_id, self.user_id)
        if is_person_heir is None:
            update.tables.users_db(self.chat_id, self.user_id, self.username, warns=warns)
        else:
            cursor.execute(f"UPDATE user SET warn={warns} WHERE user_id={self.user_id} AND chat_id={self.chat_id}")
            connect.commit()
            return warns

    def update_pydollar(self, pydollar, to_user_id, from_user_id):

        """Функция получает данные от search_person, если его там нет,
        тогда добавляем его, а если он уже есть, обновляем эту информацию"""
        count_of_pydollar_to = self.search.search_pydollar(to_user_id)
        count_of_pydollar_to = str(count_of_pydollar_to)[1:][:len(str(count_of_pydollar_to)) - 3]
        count_of_pydollar_from = self.search.search_pydollar(from_user_id)
        count_of_pydollar_from = str(count_of_pydollar_from)[1:][:len(str(count_of_pydollar_from)) - 3]
        operator = pydollar[:1]
        pydollar_for_minus = pydollar[1:]
        try:
            if operator == "-":
                if from_user_id == 1563335601 or from_user_id == 1988813101:
                    number_of_pydollar_to = int(count_of_pydollar_to) - int(pydollar_for_minus)
                    number_of_pydollar_from = int(count_of_pydollar_from) + int(pydollar_for_minus)
                else:
                    return 2
            else:
                number_of_pydollar_to = int(count_of_pydollar_to) + int(pydollar)
                number_of_pydollar_from = int(count_of_pydollar_from) - int(pydollar)
        except ValueError:
            return 1
        cursor.execute(
            f"UPDATE user SET pydollar={number_of_pydollar_to} WHERE user_id={to_user_id}")
        connect.commit()
        cursor.execute(
            f"UPDATE user SET pydollar={number_of_pydollar_from} WHERE user_id={from_user_id}")
        connect.commit()

    def update_spam(self, chat_id, spam_status):

        self.chat_id = chat_id

        is_person_heir = update.search.search_person_in_chat(self.chat_id)
        if is_person_heir is None:
            update.tables.chat_db(self.chat_id, spam_status=spam_status)
        else:
            cursor.execute(f"UPDATE chat SET spam_status={spam_status} WHERE chat_id={self.chat_id}")
            connect.commit()
            return spam_status

    def update_ban(self, chat_id, user_id, baned):

        """Функция получает количество варнов на которые нужно обновить данные, и делает это где user_id и chat_id
        равны заданным параметрам."""

        self.chat_id = chat_id
        self.user_id = user_id

        is_person_heir = self.search.search_person_in_user(self.chat_id, self.user_id)
        if is_person_heir is None:
            self.tables.users_db(self.chat_id, self.user_id, None, baned=baned)
        else:
            cursor.execute(f"UPDATE user SET baned={baned} WHERE user_id={self.user_id} AND chat_id={self.chat_id}")
            connect.commit()
            return baned

    def update_mute(self, chat_id, user_id, muted):

        """Функция получает количество варнов на которые нужно обновить данные, и делает это где user_id и chat_id
        равны заданным параметрам."""

        self.chat_id = chat_id
        self.user_id = user_id

        is_person_heir = self.search.search_person_in_user(self.chat_id, self.user_id)
        if is_person_heir is None:
            self.tables.users_db(self.chat_id, self.user_id, None, muted=muted)
        else:
            cursor.execute(f"UPDATE user SET muted={muted} WHERE user_id={self.user_id} AND chat_id={self.chat_id}")
            connect.commit()
            return muted

    def update_all_admins(self, chat_id, level):

        self.chat_id = chat_id
        self.level = level

        cursor.execute(
            f"UPDATE user SET level={self.level} WHERE"
            f" chat_id={self.chat_id}")
        connect.commit()


update = Update(0, 0, None)
