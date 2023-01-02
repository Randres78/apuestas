from sqlalchemy import Column, Integer, String
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

import db


class Usuario(db.Base):
    __tablename__ = "usuarios"
    __table_args__ = {"sqlite_autoincrement": True}
    id_usuario = Column(Integer, primary_key=True)
    usuario = Column(String(20), nullable=False, unique=True)
    email = Column(String(40), nullable=False)
    password = Column(String(80), nullable=False)

    def __init__(self, usuario, email, password):
        self.usuario = usuario
        self.email = email
        self.password = password

    def __str__(self):
        return "Usuario creado"

class LoginForm(FlaskForm):
    usuario = StringField("usuario", validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField("Clave", validators=[InputRequired(), Length(min=4, max=80)])
    remember = BooleanField("Remember me")

class RegisterForm(FlaskForm):
    usuario = StringField("Usuario", validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField("Email", validators=[InputRequired(), Email(message="Email incorrecto"), Length(min=4, max=40)])
    password = PasswordField("Clave", validators=[InputRequired(), Length(min=4, max=80)])