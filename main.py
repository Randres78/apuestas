from flask import Flask, render_template, request, redirect, url_for
import db
from models import Usuario, LoginForm, RegisterForm
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
                return redirect(url_for("dashboard"))

        return "<h3>Usuario o Clave inválida</h3>"

    return render_template("login.html", form=form)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()
    if request.method == "POST":
        user = db.session.query(Usuario).filter_by(usuario=form.usuario.data).first()
        hashed_password = generate_password_hash(form.password.data, method="sha256")
        usuario_nuevo = Usuario(usuario=form.usuario.data, email=form.email.data, password=hashed_password)
        db.session.add(usuario_nuevo)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/fase-final")
def fase_final():
    return render_template("fase-final.html")

@app.route("/tabla-posiciones")
def tabla_posiciones():
    return render_template("tabla-posiciones.html")


if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)
