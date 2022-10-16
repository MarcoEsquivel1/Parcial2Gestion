from flask import Flask, render_template, request, session, redirect, url_for, g
from llaves import *
import smtplib
import random
from functions import *

class Usuario:
    def __init__(self, id, email, password, name, age, lastname, description, username=""):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.lastname = lastname
        self.description = description
        self.age = age
        self.username = username

    def __repr__(self) -> str:
        return f'Usuario:{self.email}>'


usuarios = []
usuarios.append(Usuario(id=1, email='usuario1@email.com', name='Mario', lastname='Carranza', password='usuario1pass',
                age=31, description='Soy ingeniera en sistemas computacionales en la UPIITA', username='@mariocarranza'))
usuarios.append(Usuario(id=2, email='usuario2@email.com', name='Mery', lastname="Acevedo", password='usuario2pass', age=30,
                description='Soy arquitecta de profesion y trabajo en la empresa de arquitectura XYZ', username='@meryacevedo'))
usuarios.append(Usuario(id=3, email='usuario3@email.com', name='Cesar', lastname='Marcos', password='usuario3pass', age=29,
                description='Soy maestro de profesion y trabajo en la escuela ABC, soy profesor de matematicas, mi especialidad es la geometria', username='@cesarmarcos'))
usuarios.append(Usuario(id=4, email='usuario4@email.com', name='Heraclio', lastname='Torrents', password='usuario4pass', age=28,
                description='Soy ingeniero en sistemas computacionales y trabajo en la empresa de desarrollo de software GHI', username='@heracliotorrents'))
usuarios.append(Usuario(id=5, email='usuario5@email.com', name='Marc', lastname='Corominas', password='usuario5pass', age=23,
                description='Soy estudiante de enfermeria, cursando el 5to semestre de la carrera, me gusta mucho la medicina y la salud', username='@marccorominas'))
usuarios.append(Usuario(id=6, email='usuario6@email.com', name='Ezequiel', lastname='Patiño', password='usuario6pass', age=22,
                description='Soy estudiante de ingenieria en sistemas computacionales, cursando el 5to semestre de la carrera, me gusta mucho la programacion y la tecnologia', username='@ezequiel'))
usuarios.append(Usuario(id=7, email='usuario7@email.com', name='María Pilar', lastname='Lago', password='usuario7pass', age=21,
                description='Soy aficionada a la lectura, me gusta mucho leer libros de historia, me gusta mucho la historia de la humanidad', username='@marialago'))
usuarios.append(Usuario(id=8, email='usuario8@email.com', name='Joan', lastname='Carrera', password='usuario8pass', age=20,
                description='Soy diseñador grafico, me gusta mucho el diseño grafico, me gusta mucho la estetica y la belleza', username='@joancarrera'))
usuarios.append(Usuario(id=9, email='usuario9@email.com', name='Julio', lastname="Torres", password='usuario9pass', age=19,
                description='Soy fotografo aficionado, me gusta mucho la fotografia, actualmente estoy estudiando la carrera de fotografia', username='@juliotorres'))
usuarios.append(Usuario(id=10, email='kokirene@hotmail.com', name='Marco', lastname='Esquivel', password='marcopass', age=21,
                description='Soy estudiante de Ingenieria de Software en la Universidad Catolica de El Salvador', username='@rene_marco'))


app = Flask(__name__)
app.secret_key = '123456'


@app.before_request
def before_request():
    g.usuario = None
    if 'id_user' in session and 'logged_in' in session:
        usuario = [x for x in usuarios if x.id == session['id_user']][0]
        g.usuario = usuario


@app.route('/')
def index():
    return redirect("/login", code=302)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('id_user', None)
        email = request.form['email']
        password = request.form['password']
        usuario = [x for x in usuarios if x.email == email and x.password == password]
        if usuario:
            session['id_user'] = usuario[0].id
            session['logged_in'] = True
            return redirect("/perfil", code=302)
        else:
            return render_template('login.html', error=True)
    else:
        if g.usuario:
            return redirect("/perfil", code=302)
        else:
            return render_template('login.html', error=False)


@app.route('/logout')
def logout():
    session.pop('id_user', None)
    session.clear()
    return redirect("/login", code=302)


@app.route('/perfil')
def perfil():
    if g.usuario == None:
        return redirect(url_for('login'))
    return render_template('perfil.html')

@app.route('/send_code', methods=['POST' , 'GET'])
def scode():
    if request.method == 'POST':
        session.pop('id_user', None)
        email = request.form['email']
        usuario = [x for x in usuarios if x.email == email]
        if usuario:
            session['id_user'] = usuario[0].id
            session['email'] = usuario[0].email
            otp = random.randint(1000,10000)
            session['otp'] = otp
            """ return str(session['otp']) + " " + session['email'] """
            can = send_email(otp,usuario[0].email)
            if can:
                return redirect("/code_verify", code=302)
            else:
                return 'Error'
                return redirect("/login", code=302)
        else:
            return redirect('/send_code', code=302)
    else:
        if g.usuario:
            return redirect("/perfil", code=302)
        else:
            return render_template('code_email.html', error=False)

@app.route('/code_verify', methods=['POST' , 'GET'])
def code_verify():
    if request.method == 'POST':
        code = request.form['code']
        print(code)
        print(session['otp'])
        if str(code) == str(session['otp']):
            session['logged_in'] = True
            print('llega')
            return redirect("/perfil", code=302)
        else:
            return redirect("/code_verify", code=302)
    else:
        if g.usuario:
            return redirect("/perfil", code=302)
        else:
            return render_template('code_verify.html', error=False)

@app.route('/oauth_login', methods=['GET', 'POST'])
def github_login():
    if g.usuario:
        return redirect("/perfil", code=302)
    else:
        return redirect("https://github.com/login/oauth/authorize?client_id=74e4780ee00bdf0ef199&scope=respo", code=302)

@app.route('/oauth_callback', methods=['GET', 'POST'])
def github_callback():
    if g.usuario:
        return redirect("/perfil", code=302)
    else:
        if  request.method == 'GET':
            session.pop('id_user', None)
            email = 'kokirene@hotmail.com'
            password = 'marcopass'
            usuario = [x for x in usuarios if x.email == email and x.password == password]
        if usuario:
            session['id_user'] = usuario[0].id
            session['logged_in'] = True
            code = request.args.get('code')
            print(code)
            return redirect("/perfil", code=302)     
    
"""  """

if __name__ == '__main__':
    app.run(debug=True)


