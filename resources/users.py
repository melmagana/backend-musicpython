import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user

users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def user_index():
	
	users = models.User.select()
	user_dicts = [model_to_dict(user) for user in users]

	# REMOVE PASSWORD
	for user_dict in user_dicts:
		user_dict.pop('password')

	print(user_dicts)

	# RESPONSE
	return jsonify(
		user_dicts
	), 200


### REGISTER ROUTE -- POST ###
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

		# RESPONSE
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


		# LOGS IN USER AND STARTS A SESSION
		login_user(create_user)

		create_user_dict = model_to_dict(create_user)
		print(create_user_dict)

		print(type(create_user_dict['password']))
		create_user_dict.pop('password')


		# RESPONSE
		return jsonify(
			data=create_user_dict,
			message=f"Successfully registered user {create_user_dict['username']} with the email {create_user_dict['email']}",
			status=201
		), 201



### LOGIN ROUTE -- POST ###
@users.route('/login', methods=['POST'])
def login():

	payload = request.get_json()
	payload['name'] = payload['name']
	payload['username'] = payload['username']
	payload['email'] = payload['email']


	# LOGIC TO LOOK UP USER BY EMAIL
	try:
		user = models.User.get(models.User.email == payload['email'])

		user_dict = model_to_dict(user)


		# USER EXISTS, CHECK PASSWORD
		# 1st ARG -- THE ENCRYPTED PASSWORD YOU ARE CHECKING AGAINST
		# 2nd ARG -- THE PASSWORD ATTEMPT YOU ARE TRYING TO VERIFY
		password_is_good = check_password_hash(user_dict['password'], payload['password'])


		# LOGIC IF PASSWORD IS VALID
		if(password_is_good):
			login_user(user)

			# REMOVE PASSWORD
			user_dict.pop('password')

			# RESPONSE
			return jsonify(
				data=user_dict,
				message=f"{user_dict['username']} successfully logged in!",
				status=200
			), 200

		# LOGIC IF PASSWORD IS INVALID
		else: 
			print('password is no good')

			# RESPONSE
			return jsonify(
				data={},
				message="Email or password is invalid",
				status=401
			), 401


	# LOGIC IF USER DOES NOT EXIST
	except models.DoesNotExist:
		print('username is invalid')

		# RESPONSE
		return jsonify(
			data={},
			message="Email or password is invalid",
			status=401
		), 401



### TEMPORARY ROUTES ###
@users.route('/logged_in_user', methods=['GET'])
def currently_logged():

	print(current_user)
	print(type(current_user))


	# current_user.is_authenticated allows you to see whether a user is logged in
	if not current_user.is_authenticated:

		# RESPONSE
		return jsonify(
			data={},
			message="No user is currently logged in",
			status=401
		), 401

	# ACCESS TO CURRENTLY LOGGED USER
	else:
		user_dict = model_to_dict(current_user)
		user_dict.pop('password')

		# RESPONSE
		return jsonify(
			data=user_dict,
			message=f"Currently logged in as user {user_dict['username']} with the email {user_dict['email']}",
			status=200
		), 200



### LOGOUT ROUTE -- GET ###
@users.route('/logout', methods=['GET'])
def logout():

	logout_user()

	# RESPONSE
	return jsonify(
		data={},
		message="Successfully logged out!",
		status=200
	), 200
