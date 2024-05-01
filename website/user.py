from flask import Blueprint
from flask_login import current_user
from .models import User
from . import cipher_suite


user = Blueprint('user', __name__)

def getmatricula():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        if user.matricula:
            decrypted_matricula = cipher_suite.decrypt(user.matricula.encode()).decode()
            return decrypted_matricula
        else:
            return None
