class User:
    def __init__(self, user_id, username):
        self.__user_id = user_id
        self.__username = username

    def get_id(self):
        return self.__user_id

    def get_username(self):
        return self.__username


class Lecturer(User):
    pass


class CampusAdministrator(User):
    pass


class SystemOperator(User):
    pass
