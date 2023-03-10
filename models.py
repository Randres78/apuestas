from sqlalchemy import Column, Integer, String, ForeignKey
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FieldList, SelectField, HiddenField, FormField, Form
from wtforms.validators import InputRequired, Email, Length

import db


class Usuario(db.Base):
    __tablename__ = "usuarios"
    __table_args__ = {"sqlite_autoincrement": True}
    id_usuario = Column(Integer, primary_key=True)
    usuario = Column(String(20), nullable=False, unique=True)
    email = Column(String(40), nullable=False)
    password = Column(String(80), nullable=False)
    puntaje = Column(Integer)

    def __init__(self, usuario, email, password):
        self.usuario = usuario
        self.email = email
        self.password = password

    def __str__(self):
        return "Usuario creado"

class Grupo(db.Base):
    __tablename__ = "grupos"
    __table_args__ = {"sqlite_autoincrement": True}
    id_grupo = Column(Integer, primary_key=True)
    letra = Column(String(1), nullable=False, unique=True)
    
    def __init__(self, letra):
        self.letra = letra

    def __str__(self):
        return "Equipo creado"

class EquipoXGrupo(db.Base):
    __tablename__ = "equipos_x_grupos"
    __table_args__ = {"sqlite_autoincrement": True}
    id_equipo_x_grupo = Column(Integer, primary_key=True)
    id_equipo = Column(Integer, ForeignKey("equipos.id_equipo"), nullable=False)
    id_grupo = Column(Integer, ForeignKey("grupos.id_grupo"), nullable=False)
    
    def __init__(self, id_equipo, id_grupo):
        self.id_equipo = id_equipo
        self.id_grupo = id_grupo

    def __str__(self):
        return "Equipo creado"

class Equipo(db.Base):
    __tablename__ = "equipos"
    __table_args__ = {"sqlite_autoincrement": True}
    id_equipo = Column(Integer, primary_key=True)
    nombre = Column(String(30), nullable=False, unique=True)
    
    def __init__(self, id_equipo, nombre):
        self.id_equipo = id_equipo
        self.nombre = nombre

    def __str__(self):
        return "Equipo creado"

class Prediccion(db.Base):
    __tablename__ = "predicciones"
    __table_args__ = {"sqlite_autoincrement": True}
    id_prediccion = Column(Integer, primary_key=True)
    id_grupo = Column(Integer, ForeignKey("grupos.id_grupo"), nullable=False)
    equipo_clasificado_1 = Column(Integer, ForeignKey("equipos.id_equipo"), nullable=False)
    equipo_clasificado_2 = Column(Integer, ForeignKey("equipos.id_equipo"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    def __init__(self, id_grupo, equipo_clasificado_1, equipo_clasificado_2, id_usuario):
        self.id_grupo = id_grupo
        self.equipo_clasificado_1 = equipo_clasificado_1
        self.equipo_clasificado_2 = equipo_clasificado_2
        self.id_usuario = id_usuario

    def __str__(self):
        return "Predicci??n creada"

class PrediccionRonda16(db.Base):
    __tablename__ = "predicciones_R16"
    __table_args__ = {"sqlite_autoincrement": True}
    id_prediccionRonda16 = Column(Integer, primary_key=True)
    partido = Column(Integer, nullable=False)
    id_equipo = Column(Integer, ForeignKey("equipos.id_equipo"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    def __init__(self, partido, id_equipo, id_usuario):
        self.partido = partido
        self.id_equipo = id_equipo
        self.id_usuario = id_usuario
    def __str__(self):
        return "Predicci??n creada"

class PrediccionCuartos(db.Base):
    __tablename__ = "predicciones_cuartos"
    __table_args__ = {"sqlite_autoincrement": True}
    id_prediccionCuartos = Column(Integer, primary_key=True)
    partido_cuartos = Column(Integer, nullable=False)
    id_equipo = Column(Integer, ForeignKey("equipos.id_equipo"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    def __init__(self, partido_cuartos, id_equipo, id_usuario):
        self.partido_cuartos = partido_cuartos
        self.id_equipo = id_equipo
        self.id_usuario = id_usuario

    def __str__(self):
        return "Predicci??n Creada"

class PrediccionSemifinal(db.Base):
    __tablename__ = "predicciones_semifinal"
    __table_args__ = {"sqlite_autoincrement": True}
    id_prediccionSemi = Column(Integer, primary_key=True)
    partido_semi = Column(Integer, nullable=False)
    id_equipo = Column(Integer, ForeignKey("equipos.id_equipo"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    def __init__(self, partido_semi, id_equipo, id_usuario):
        self.partido_semi = partido_semi
        self.id_equipo = id_equipo
        self.id_usuario = id_usuario

    def __str__(self):
        return "Predicci??n Creada"

class PrediccionFinal(db.Base):
    __tablename__ = "predicciones_final"
    __table_args__ = {"sqlite_autoincrement": True}
    id_prediccionFinal = Column(Integer, primary_key=True)
    partido_final = Column(Integer, nullable=False)
    id_equipo = Column(Integer, ForeignKey("equipos.id_equipo"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    def __init__(self, partido_final, id_equipo, id_usuario):
        self. partido_final = partido_final
        self.id_equipo = id_equipo
        self.id_usuario = id_usuario

    def __str__(self):
        return "Predicci??n Creada"
'''
TAREA1: Crear una tabla llamada:
PrediccionCuartos(
    id_prediccionCuartos,
    partido: (1, ...4),
    id_equipo,
    id_usuario
)
'''

class LoginForm(FlaskForm):
    usuario = StringField("usuario", validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField("Clave", validators=[InputRequired(), Length(min=4, max=80)])
    remember = BooleanField("Remember me")

class RegisterForm(FlaskForm):
    usuario = StringField("Usuario", validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField("Email", validators=[InputRequired(), Email(message="Email incorrecto"), Length(min=4, max=40)])
    password = PasswordField("Clave", validators=[InputRequired(), Length(min=4, max=80)])
