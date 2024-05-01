from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from . import cipher_suite



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(request.referrer or url_for('views.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Senha incorreta.', category='error')
        else:
            flash('Email não existe.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(request.referrer or url_for('views.home'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(request.referrer or url_for('views.home'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user_Email = User.query.filter_by(email=email).first()
        user_Username = User.query.filter_by(username=username).first()
        if user_Username:
            flash('Nome de usuário já registrado.', category='error')
        elif user_Email:
            flash('Email já registrado.', category='error')
        elif len(password1) < 8 or len(password1) > 128:
            flash('A senha deve conter entre 8 e 128 caracteres.', category='error')
        elif password1 != password2:
            flash('Senhas não coincidem.', category='error')
        else:
            new_user = User(username=username, email=email, password=generate_password_hash(password1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password0 = request.form.get('password0')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        matricula = request.form.get('matricula')

        user = User.query.get(current_user.id)

        # Update Username
        if username and username != user.username:
            user_Username = User.query.filter_by(username=username).first()
            if user_Username:
                flash('Nome de usuário já registrado.', category='error')
            else:
                user.username = username
                flash('Nome de usuário alterado com sucesso.', category='success')

        # Update Email
        if email and email != user.email:
            user_Email = User.query.filter_by(email=email).first()
            if user_Email:
                flash('Email já registrado.', category='error')
            else:
                user.email = email
                flash('Email alterado com sucesso.', category='success')

        # Update Password
        if password0 and password1 and password2:
            if not check_password_hash(user.password, password0):
                flash('Senha incorreta.', category='error')
            elif password0 == password1:
                flash('A senha antiga e a nova senha não podem ser iguais.', category='error')    
            elif password1 != password2:
                flash('Senhas novas não coincidem.', category='error')
            elif len(password1) < 8 or len(password1) > 128:
                flash('A senha deve conter entre 8 e 128 caracteres.', category='error')
            else:
                user.password = generate_password_hash(password1, method='scrypt')
                flash('Senha alterada com sucesso.', category='success')

        # Update matricula
        if matricula and matricula != user.matricula:
            encrypted_matricula = cipher_suite.encrypt(matricula.encode()).decode()
            user.matricula = encrypted_matricula
            flash('Matrícula alterada com sucesso.', category='success')
        
        db.session.commit()

    return render_template("profile.html", user=current_user)