from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Matricula, Curso
from . import db


views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    cursos = Curso.query.all()
    return render_template("home.html", user=current_user, cursos=cursos)


@views.route('/adduser', methods=['POST'])
@login_required
def adduser():
    if request.method == 'POST':
        matricula = request.form.get('matricula')
        curso_id = request.form.get('curso_id')
        
        curso = Curso.query.get(curso_id)
        if not curso:
            flash('Curso não encontrado.', category='error')
            return render_template("profile.html", user=current_user)
        
        existing_matricula = Matricula.query.filter_by(matricula=matricula).first()

        if existing_matricula:
            # Se a matrícula já estiver associada a este curso específico
            if curso in existing_matricula.cursos:
                flash('Usuário já cadastrado neste curso.', category='error')
            else:
                # Associe a matrícula existente a este curso
                curso.matriculas.append(existing_matricula)
                db.session.commit()
                flash('Usuário cadastrado com sucesso no curso.', category='success')
        else:
            new_matricula = Matricula(matricula=matricula)
            curso.matriculas.append(new_matricula)
            db.session.add(new_matricula)
            db.session.commit()
            flash('Usuário cadastrado com sucesso.', category='success')

    return redirect(url_for('views.home'))

@views.route('/addtable', methods=['POST'])
@login_required
def addtable():
    if request.method == 'POST':
        nome_curso = request.form.get('nome_curso')
        
        # Verificar se o curso já existe
        existing_curso = Curso.query.filter_by(nome=nome_curso).first()

        if existing_curso:
            flash('Curso já existe.', category='error')
        else:
            new_curso = Curso(nome=nome_curso)
            db.session.add(new_curso)
            db.session.commit()
            flash('Curso adicionado com sucesso.', category='success')
            
    return redirect(url_for('views.home'))

