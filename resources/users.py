import models

from flask import Blueprint

users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def test_user():
	return 'user resource works'