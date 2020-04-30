import models

from flask import Blueprint, request

users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def test_user():
	return 'user resource works'


@users.route('/register', methods=['POST'])
def register():
	print(request.get_json())
	return 'check terminal'