class User:
    def __init__(self, username, email, password):
        self.__username = username
        self.__email = email
        self.__password = password

        self.__level1Status = False
        self.__level2Status = False

    def get_username(self):
        return self.__username

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def set_username(self, username):
        self.__username = username

    def set_email(self, email):
        self.__email = email

