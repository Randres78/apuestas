from flask import Flask, render_template, request, redirect, url_for, session as flask_session
import db
from models import Usuario, LoginForm, RegisterForm, Grupo, Prediccion, EquipoXGrupo, Equipo, DashboardForm
from werkzeug.security import generate_password_hash, check_password_hash

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

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    form = DashboardForm()
    '''
    TAREA: 
    1) Consultar los grupos con sus respectivos equipos haciendo uso de sqlAlchemy
    grupos = db.session.query(Grupo) + los equipos en cada grupo
    
    2) Consultar las predicciones
    predicciones = db.session.query(Prediccion)
    
    3) if request.method == 'POST':
        Como esta singup, guardar los marcadores seleccionados por el usuario
    
    MAÑANA:
    1) Obtener en el login el id del usuario, para filtar las predicciones por usuario
    2) No permitir que el usuario ingrese sus marcadores de nuevo
    '''

    grupos = (db.session.query(Grupo, Equipo)
              .join(EquipoXGrupo, Grupo.id_grupo==EquipoXGrupo.id_grupo)
              .join(Equipo, EquipoXGrupo.id_equipo==Equipo.id_equipo)).all()
    predicciones = db.session.query(Prediccion).filter_by(id_usuario=flask_session["id_usuario"]).all()
    form.grupos = grupos
    form.predicciones = predicciones
    if request.method == "POST":
        seleccion_usuario = Prediccion(Prediccion.id_prediccion)
        db.session.add(seleccion_usuario)
        db.session.commit()
        return redirect(url_for("fase-final"))
    return render_template("dashboard.html", form=form)

@app.route("/fase-final")
def fase_final():
    return render_template("fase-final.html")

@app.route("/tabla-posiciones")
def tabla_posiciones():
    return render_template("tabla-posiciones.html")


if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)
