import flask_login
import werkzeug.security as safe

class UserDto(flask_login.UserMixin):
    def __init__(self, name, username, password):
        self._name = name
        self._username = username
        self._password = safe.generate_password_hash(password)

    @property
    def name(self):
        return self._name

    @property
    def username(self):
        return self._username

    def chk_password(self, pswd):
        return safe.check_password_hash(self._password, pswd)

    def get_id(self):
        return self.username

    @staticmethod
    def find(srp: "Sirope", username: str) -> "UserDto|None":
        return srp.find_first(UserDto, lambda u: u.username == username)

    @staticmethod
    def current_user():
        toret = flask_login.current_user

        if toret.is_anonymous:
            flask_login.logout_user()
            toret = None

        return toret

    def __str__(self):
        return f'Nombre: {self.name} | Usuario: {self.username} | Clave: {self._password}'