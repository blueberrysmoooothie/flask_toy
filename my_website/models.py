from flask import session


class User:
    user_list_ = []
    user_data_ = {}

    @classmethod
    def sign_in(cls, id, password):
        if id in User.user_list_:
            user_info = User.user_data_[id]

            if password == user_info["user_password_"]:
                session["user_name_"] = user_info["user_name_"]
                session["user_id_"] = id
                return True
        return False

    @classmethod
    def logout(cls):
        session.clear()

    @classmethod
    def add_user_info(cls, nickname, userid, password1):
        User.user_list_.append(userid)
        User.user_data_[userid] = {"user_name_": nickname, "user_password_": password1}

    @classmethod
    def dup_check(cls, userid):
        if userid in User.user_list_:
            return True
        return False
