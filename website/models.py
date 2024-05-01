from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Tabela de associação
curso_matricula = db.Table('curso_matricula',
    db.Column('curso_id', db.Integer, db.ForeignKey('curso.id'), primary_key=True),
    db.Column('matricula_id', db.Integer, db.ForeignKey('matricula.id'), primary_key=True)
)


class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128), unique=True) # Nome do curso
    matriculas = db.relationship('Matricula', secondary=curso_matricula, backref=db.backref('cursos', lazy=True))


class Matricula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(128), unique=True) # Mantendo a matrícula única
    date = db.Column(db.DateTime(timezone=True), default=func.now()) # Registration time


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    matricula = db.Column(db.String(128))