from flask import Flask, render_template, request, redirect, url_for, session as flask_session
import db
from models import Usuario, LoginForm, RegisterForm, Grupo, Prediccion, EquipoXGrupo, Equipo, PrediccionRonda16
from werkzeug.security import generate_password_hash, check_password_hash
from collections import namedtuple
from sqlalchemy.orm import aliased

app = Flask(__name__) # En app se encuentra nuestro servidor web de Flask. Debe estar arriba de todo
app.config["SECRET_KEY"] = "clavesecreta"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'POST':
        user = db.session.query(Usuario).filter_by(usuario=form.usuario.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                flask_session["id_usuario"] = user.id_usuario
                flask_session["nombre_usuario"] = user.usuario
                return redirect(url_for("dashboard"))

        return "<h3>Usuario o Clave inválida</h3>"

    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET"])
def logout():
    flask_session.pop('id_usuario',None)
    flask_session.pop('nombre_usuario',None)
    return redirect(url_for('login'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()
    if request.method == "POST":
        hashed_password = generate_password_hash(form.password.data, method="sha256")
        usuario_nuevo = Usuario(usuario=form.usuario.data, email=form.email.data, password=hashed_password)
        db.session.add(usuario_nuevo)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)

def get_select_data(id_grupo):
    equipos = (db.session.query(Equipo)
            .join(EquipoXGrupo, EquipoXGrupo.id_equipo==Equipo.id_equipo)
            .filter_by(id_grupo = id_grupo)
            ).all()
    Equipo_tuple = namedtuple('Equipo_tuple', ['id_equipo', 'nombre'])
    select_data = []
    for equipo in equipos:
        select_data.append(Equipo_tuple(equipo.id_equipo, equipo.nombre))
    return select_data

def get_group_data():
    grupos = db.session.query(Grupo).all()
    Grupo_data = namedtuple('Grupo_data', ['indice', 'id_grupo', 'letra', 'opciones_equipos'])
    grupos_data = []
    for i, grupo in enumerate(grupos):
        grupos_data.append(Grupo_data(i, grupo.id_grupo, grupo.letra, get_select_data(grupo.id_grupo)))
    equipo_2 = aliased(Equipo)
    predicciones = (db.session.query(Prediccion, Grupo.letra, Equipo.nombre.label('equipo_clasificado_1'), equipo_2.nombre.label('equipo_clasificado_2'))
                    .filter_by(id_usuario=flask_session["id_usuario"])
                    .join(Grupo, Prediccion.id_grupo == Grupo.id_grupo)
                    .join(Equipo, Prediccion.equipo_clasificado_1 == Equipo.id_equipo)
                    .join(equipo_2, Prediccion.equipo_clasificado_2 == equipo_2.id_equipo)
                    ).all()
    return { 'grupos': grupos_data, 'predicciones': predicciones }

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "id_usuario" not in flask_session:
        return redirect(url_for('login'))
    if request.method == "GET":
        data = get_group_data()
        return render_template("dashboard.html", nombre_usuario=flask_session["nombre_usuario"], data = data)
    elif request.method == "POST":
        for i in range(8):
            db.session.add(Prediccion(
                request.form[f'grupo_{i}'],
                request.form[f'equipo_clasificado_1_{i}'],
                request.form[f'equipo_clasificado_2_{i}'],
                flask_session["id_usuario"]
            ))
            db.session.commit()
        return redirect(url_for("fase_final"))
    
def get_predicciones():
    equipo_2 = aliased(Equipo)
    predicciones = db.session.query(Prediccion, Grupo.letra, Equipo.id_equipo.label('id_equipo_clasificado_1'), Equipo.nombre.label('equipo_clasificado_1'), equipo_2.id_equipo.label('id_equipo_clasificado_2'), equipo_2.nombre.label('equipo_clasificado_2'))\
                    .filter_by(id_usuario=flask_session["id_usuario"])\
                    .join(Grupo, Prediccion.id_grupo == Grupo.id_grupo)\
                    .join(Equipo, Prediccion.equipo_clasificado_1 == Equipo.id_equipo)\
                    .join(equipo_2, Prediccion.equipo_clasificado_2 == equipo_2.id_equipo)\
                    .all()
    equipos_fase2 = {}
    
    for prediccion in predicciones:
        equipos_fase2['1ro {}'.format(prediccion.letra)] = {
            'id': prediccion.id_equipo_clasificado_1,
            'nombre': prediccion.equipo_clasificado_1
        }
        equipos_fase2['2do {}'.format(prediccion.letra)] = {
            'id': prediccion.id_equipo_clasificado_2,
            'nombre': prediccion.equipo_clasificado_2
        }
    
    partidos_fase2 = [
        {
            'id': 1,
            'equipo1': equipos_fase2['1ro A'],
            'equipo2': equipos_fase2['2do B']
        },
        {
            'id': 2,
            'equipo1': equipos_fase2['1ro B'],
            'equipo2': equipos_fase2['2do A']
        },
        {
            'id': 3,
            'equipo1': equipos_fase2['1ro C'],
            'equipo2': equipos_fase2['2do D']
        },
        {
            'id': 4,
            'equipo1': equipos_fase2['1ro D'],
            'equipo2': equipos_fase2['2do C']
        },
        {
            'id': 5,
            'equipo1': equipos_fase2['1ro E'],
            'equipo2': equipos_fase2['2do F']
        },
        {
            'id': 6,
            'equipo1': equipos_fase2['1ro F'],
            'equipo2': equipos_fase2['2do E']
        },
        {
            'id': 7,
            'equipo1': equipos_fase2['1ro G'],
            'equipo2': equipos_fase2['2do H']
        },
        {
            'id': 8,
            'equipo1': equipos_fase2['1ro H'],
            'equipo2': equipos_fase2['2do G']
        }
    ]
    return partidos_fase2

@app.route("/fase-final", methods=['GET', 'POST'])
def fase_final():
    if "id_usuario" not in flask_session:
        return redirect(url_for('login'))
    
    partidos_fase2 = None
    partidos_cuartos = None
    prediccionesR16 = (db.session.query(PrediccionRonda16.partido, Equipo.id_equipo, Equipo.nombre.label('nombre_equipo'))
                        .filter_by(id_usuario = flask_session["id_usuario"])
                        .join(Equipo, PrediccionRonda16.id_equipo == Equipo.id_equipo)
                    ).all()
    if len(prediccionesR16) == 0:
        partidos_fase2 = get_predicciones()
    else:
        equipos_cuartos = {}
        for pred16 in prediccionesR16:
            equipos_cuartos[pred16.partido] = {
                'id_equipo': pred16.id_equipo,
                'nombre_equipo': pred16.nombre_equipo
            }
        partidos_cuartos = [
            {
                'id': 1,
                'id_1': 1,
                'id_2': 3,
                'equipo1': equipos_cuartos[1],
                'equipo2': equipos_cuartos[3]
            },
            {
                'id': 2,
                'id_1': 2,
                'id_2': 4,
                'equipo1': equipos_cuartos[2],
                'equipo2': equipos_cuartos[4]
            },
            {
                'id': 3,
                'id_1': 5,
                'id_2': 7,
                'equipo1': equipos_cuartos[5],
                'equipo2': equipos_cuartos[7]
            },
            {
                'id': 4,
                'id_1': 6,
                'id_2': 8,
                'equipo1': equipos_cuartos[6],
                'equipo2': equipos_cuartos[8]
            }
        ]
    
    if request.method == "POST":

        # Se almacena la ronda de 16
        if 'partido_1' in request.form:
            for i in range(1, 9):
                db.session.add(PrediccionRonda16(
                i,
                request.form[f'partido_{i}'],
                flask_session["id_usuario"]
                ))
        # Se almacena la ronda de cuartos
        elif 'partido_cuartos_1' in request.form:
            pass

        db.session.commit()

    '''
    Guardar los resultados de los partidos en la tabla PrediccionRonda16,
    mira la línea 82.
    '''
        
    return render_template("fase-final.html", nombre_usuario=flask_session["nombre_usuario"], partidos_fase2 = partidos_fase2, prediccionesR16 = prediccionesR16, partidos_cuartos = partidos_cuartos)

@app.route("/tabla-posiciones")
def tabla_posiciones():
    return render_template("tabla-posiciones.html")


if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)
