from flask import Flask, make_response, render_template, request, redirect, url_for, session as flask_session
import db
from models import Usuario, LoginForm, RegisterForm, Grupo, Prediccion, EquipoXGrupo, Equipo, PrediccionRonda16, PrediccionCuartos, PrediccionSemifinal, PrediccionFinal
from werkzeug.security import generate_password_hash, check_password_hash
from collections import namedtuple
from sqlalchemy.orm import aliased
from business_logic import get_partido_final, get_partidos_R16, get_partidos_cuartos, get_partidos_semi, guardar_prediccion, guardar_puntaje, obtener_puntaje

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

@app.route("/calcular_puntaje", methods=['GET'])
def calcular_puntaje():
    puntaje = obtener_puntaje(flask_session["id_usuario"])
    guardar_puntaje(flask_session["id_usuario"], puntaje)
    
    response = make_response("Guardando el puntaje ...", 200)
    response.mimetype = "text/plain"
    return response

@app.route("/fase-final", methods=['GET', 'POST'])
def fase_final(i=None):
    if "id_usuario" not in flask_session:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        guardar_prediccion(flask_session["id_usuario"], request.form)

    partidos_faseR16 = []
    partidos_cuartos = []
    partidos_semi = []
    partidos_final = []
    partidos_faseR16 = []
    prediccionesCuartos = None
    prediccionesSemifinal = None
    prediccionesFinal = None
    
    equipo_2 = aliased(Equipo)
    predicciones_grupos = db.session.query(Prediccion, Grupo.letra, Equipo.id_equipo.label('id_equipo_clasificado_1'), Equipo.nombre.label('equipo_clasificado_1'), equipo_2.id_equipo.label('id_equipo_clasificado_2'), equipo_2.nombre.label('equipo_clasificado_2'))\
                    .filter_by(id_usuario=flask_session["id_usuario"])\
                    .join(Grupo, Prediccion.id_grupo == Grupo.id_grupo)\
                    .join(Equipo, Prediccion.equipo_clasificado_1 == Equipo.id_equipo)\
                    .join(equipo_2, Prediccion.equipo_clasificado_2 == equipo_2.id_equipo)\
                    .all()
    
    # Predicciones R16
    prediccionesR16 = (db.session.query(PrediccionRonda16.partido, Equipo.id_equipo, Equipo.nombre.label('nombre_equipo'))
                        .filter_by(id_usuario = flask_session["id_usuario"])
                        .join(Equipo, PrediccionRonda16.id_equipo == Equipo.id_equipo)
                    ).all()
    if len(prediccionesR16) == 0:
        partidos_faseR16 = get_partidos_R16(predicciones_grupos)
    else:
        # Predicciones Cuartos
        prediccionesCuartos = (db.session.query(PrediccionCuartos.partido_cuartos, Equipo.id_equipo, Equipo.nombre.label('nombre_equipo'))
                            .filter_by(id_usuario=flask_session["id_usuario"])
                            .join(Equipo, PrediccionCuartos.id_equipo == Equipo.id_equipo)
                            .all()
                            )
        if len(prediccionesCuartos) == 0:
            partidos_cuartos = get_partidos_cuartos(prediccionesR16)
        else:
            # Predicciones Semifinal
            prediccionesSemifinal = (db.session.query(PrediccionSemifinal.partido_semi, Equipo.id_equipo, Equipo.nombre.label("nombre_equipo"))
                             .filter_by(id_usuario=flask_session["id_usuario"])
                             .join(Equipo, PrediccionSemifinal.id_equipo == Equipo.id_equipo)
                             .all()
                             )
            if len(prediccionesSemifinal) == 0:
                partidos_semi = get_partidos_semi(prediccionesCuartos)
            else:
                # Predicciones Final
                prediccionesFinal = (db.session.query(PrediccionFinal.partido_final, Equipo.id_equipo, Equipo.nombre.label("nombre_equipo"))
                                    .filter_by(id_usuario=flask_session["id_usuario"])
                                    .join(Equipo, PrediccionFinal.id_equipo == Equipo.id_equipo)
                                    .first()
                                    )
                if not prediccionesFinal:
                    partidos_final = get_partido_final(prediccionesSemifinal)

    return render_template("fase-final.html", nombre_usuario=flask_session["nombre_usuario"],
                           partidos_faseR16 = partidos_faseR16, prediccionesR16 = prediccionesR16,
                           partidos_cuartos = partidos_cuartos, prediccionesCuartos = prediccionesCuartos,
                           partidos_semi = partidos_semi, prediccionesSemifinal = prediccionesSemifinal,
                           partidos_final = partidos_final, prediccionesFinal=prediccionesFinal
                           )

@app.route("/tabla-posiciones")
def tabla_posiciones():
    return render_template("tabla-posiciones.html")


if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)
