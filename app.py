import flask
from flask import Flask
import flask_login
import sirope
from sirope import OID
import json
from model import UserDto
from model import LibroDto
from model import ResenhaDto

app = Flask(__name__)


def create_app():
    flapp = flask.Flask(__name__)
    sirp = sirope.Sirope()
    lgmg = flask_login.login_manager.LoginManager()

    flapp.config.from_file("config.json", json.load)
    lgmg.init_app(flapp)
    return flapp, sirp, lgmg


app, srp, lm = create_app()


@lm.user_loader
def user_loader(uid: str) -> UserDto | None:
    return UserDto.find(srp, uid)


@app.route('/')
def get_index():
    usr = UserDto.current_user()
    sust = {
        "usr": usr
    }
    if not usr:
        return flask.render_template("login.html", **sust)
    else:
        libros = list(srp.load_last(LibroDto, 5))
        sust = {
            "usr": usr,
            "libros": libros,
            "libros_oids": {l.__oid__: srp.safe_from_oid(l.__oid__) for l in libros}
        }
        return flask.render_template("listado_libros.html", **sust)


@app.route('/login', methods=['POST'])
def login():
    username = flask.request.form.get("edUsername")
    password = flask.request.form.get("edPassword")

    if not username:
        flask.flash("Tiene que introducir su login.")
        flask.redirect('/login')
    elif not password:
        flask.flash("Tiene que introducir su password.")
        flask.redirect('/login')
    else:
        usr = UserDto.find(srp, username)
        if not usr:
            flask.flash("No existe este usuario en el sistema.")
            return flask.redirect('/')
        elif not usr.chk_password(password):
            flask.flash("La contraseña introducida no es correcta.")
            return flask.redirect('/')
        else:
            flask_login.login_user(usr)
            return flask.redirect('/')

    sust = {
        "username": username,
        "password": password
    }

    return flask.render_template('login.html', **sust)


@app.route('/sing_up', methods=['GET', 'POST'])
def registrarse():
    name = flask.request.form.get("edName")
    username = flask.request.form.get("edUsername")
    password = flask.request.form.get("edPassword")

    if not name:
        flask.flash("Para registrarse tiene que introducir un nombre.")
        flask.redirect('/login')
    elif not username:
        flask.flash("Para registrarse tiene que introducir un nombre de usuario.")
        flask.redirect('/login')
    elif not password:
        flask.flash("Para registrarse tiene que introducir una clave.")
        flask.redirect('/login')
    else:
        usr = UserDto.find(srp, username)
        if not usr:
            if username and password is not None:
                usr = UserDto(name, username, password)
                srp.save(usr)
                flask_login.login_user(usr)
                return flask.redirect("/")
        else:
            flask.flash("Ya existe este usuario en el sistema.")

    sust = {
        "username": username,
        "password": password,
        "name": name
    }

    return flask.render_template('login.html', **sust)


@app.route('/inicio')
def inicio():
    usr = UserDto.current_user()
    sust = {
        "usr": usr
    }
    return flask.render_template("inicio.html", **sust)


@app.route('/lista_libros')
def lista_libros():
    usr = UserDto.current_user()
    libros = list(srp.load_all(LibroDto))
    sust = {
        "usr": usr,
        "libros": libros,
        "libros_oids": {l.__oid__: srp.safe_from_oid(l.__oid__) for l in libros}
    }
    return flask.render_template("listado_libros.html", **sust)


@app.route('/elimina_libro', methods=['GET', 'POST'])
def elimina_libro():
    usr = UserDto.current_user()
    oid = flask.request.form.get("edOid")

    if not oid:
        flask.flash("OID not found")
        return flask.redirect("/lista_libros")

    else:
        oid_parts = oid.split("@")
        srp.delete(OID.from_pair((oid_parts[0], oid_parts[1])))

        libros = list(srp.load_all(LibroDto))

        sust = {
            "usr": usr,
            "libros": libros,
            "libros_oids": {l.__oid__: srp.safe_from_oid(l.__oid__) for l in libros}
        }
        return flask.render_template("listado_libros.html", **sust)


@app.route('/guarda_libro', methods=['POST'])
def guarda_libro():
    titulo = flask.request.form.get("edTitulo")
    autor = flask.request.form.get("edAutor")
    isbn = flask.request.form.get("edIsbn")
    url = flask.request.form.get("edUrl")
    argumento = flask.request.form.get("edArgumento")

    # Chk datos (anhadir más)
    if not titulo:
        flask.flash("Introduzca un título.")
        return flask.redirect("/")
    elif not autor:
        flask.flash("Introduzca un autor")
        return flask.redirect("/")
    elif not isbn:
        flask.flash("Introduzca un ISBN")
        return flask.redirect("/")
    elif not url:
        flask.flash("Introduzca una URL")
        return flask.redirect("/")
    elif not argumento:
        flask.flash("Introduzca un argumento")
        return flask.redirect("/")

    # Guardar
    srp.save(LibroDto(titulo, autor, isbn, url, argumento))

    return flask.redirect('/lista_libros')


@app.route('/edita_libro', methods=['POST'])
def edita_libro():

    titulo = flask.request.form.get("edTitulo")
    autor = flask.request.form.get("edAutor")
    argumento = flask.request.form.get("edArgumento")
    url = flask.request.form.get("edUrl")
    safe_oid = flask.request.form.get("edOid")

    if not safe_oid:
        return flask.flash("modifica(): OID no encontrado")

    libro = srp.load(srp.oid_from_safe(safe_oid))

    if not titulo:
        flask.flash("Introduzca un titulo")
        return flask.redirect("/lista_libros")
    elif not autor:
        flask.flash("Introduzca un autor")
        return flask.redirect("/lista_libros")
    elif not argumento:
        flask.flash("Introduzca un argumento")
        return flask.redirect("/lista_libros")
    elif not url:
        flask.flash("Introduzca una URL")
        return flask.redirect("/lista_libros")

    if not libro:
        return flask.flash("edita_libro(): libro no encontrado")

    libro.titulo = titulo
    libro.autor = autor
    libro.argumento = argumento
    libro.url = url

    srp.save(libro)

    return flask.redirect('/lista_libros')


@app.route('/lista_resenhas')
def lista_resenhas():
    usr = UserDto.current_user()
    resenhas = list(srp.load_all(ResenhaDto))
    sust = {
        "usr": usr,
        "resenhas": resenhas,
        "resenhas_oids": {r.__oid__: srp.safe_from_oid(r.__oid__) for r in resenhas}
    }

    return flask.render_template("listado_resenhas.html", **sust)


@app.route('/guarda_resenha', methods=['POST'])
def guarda_resenha():
    titulo = flask.request.form.get("edTitulo")
    url = flask.request.form.get("edUrl")
    autor = UserDto.current_user()
    opinion = flask.request.form.get("edOpinion")

    # Chk datos (anhadir más)
    if not titulo:
        flask.flash("Introduzca un titulo")
        return flask.redirect("/lista_resenhas")
    elif not url:
        flask.flash("Introduzca una URL")
        return flask.redirect("/lista_resenhas")
    elif not autor:
        flask.flash("Introduzca un autor")
        return flask.redirect("/lista_resenhas")
    elif not opinion:
        flask.flash("Introduzca una reseña.")
        return flask.redirect("/lista_resenhas")

    resenha = ResenhaDto(titulo, url, autor.username, opinion)

    srp.save(resenha)

    return flask.redirect('/lista_resenhas')


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect("/")


@lm.unauthorized_handler
def unauthorized():
    return "No autorizado", 401


if __name__ == '__main__':
    app.run()
