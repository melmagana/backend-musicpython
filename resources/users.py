import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash
from playhouse.shortcuts import model_to_dict

users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def test_user():
	return 'user resource works'


@users.route('/register', methods=['POST'])
def register():
	
	payload = request.get_json()
	payload['name'] = payload['name']
	payload['username'] = payload['username'].lower()
	payload['email'] = payload['email'].lower()
	print(payload)


	# LOGIC TO SEE IF USER EXISTS
	try:
		models.User.get(models.User.email == payload['email'])

		return jsonify(
			data={},
			message=f"A user with the email {payload['email']} already exists",
			status=401
		), 401


	except models.DoesNotExist:

		# scramble password with bcrypt
		pw_hash = generate_password_hash(payload['password'])


		# CREATE USER
		create_user = models.User.create(
			name=payload['name'],
			username=payload['username'],
			email=payload['email'],
			password=pw_hash
		)

		print(create_user)

		create_user_dict = model_to_dict(create_user)
		print(create_user_dict)

		print(type(create_user_dict['password']))
		create_user_dict.pop('password')


		return jsonify(
			data=create_user_dict,
			message=f"Successfully registered user {create_user_dict['username']} with the email {create_user_dict['email']}",
			status=201
		), 201