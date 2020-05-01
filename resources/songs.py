import models

from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

songs = Blueprint('songs', 'songs')

### SONG INDEX ROUTE (ALL USERS) -- GET ###
@songs.route('/', methods=['GET'])
@login_required
def songs_index():
	
	result = models.Song.select()
	print(result)

	song_dicts = [model_to_dict(song) for song in result]

	for song_dict in song_dicts:
		song_dict['posted_by'].pop('password')

	print('- ' * 20)
	print('here is song_dicts')
	print(song_dicts)

	# RESPONSE
	return jsonify({
		'data': song_dicts,
		'message': f"Successfully found {len(song_dicts)} songs",
		'status': 200
	}), 200



### SONG INDEX ROUTE (LOGGED IN USER) -- GET ###
@songs.route('/my_songs', methods=['GET'])
@login_required
def my_songs_index():

	current_user_song_dicts = [model_to_dict(song) for song in current_user.songs]

	for song_dict in current_user_song_dicts:
		song_dict['posted_by'].pop('password')
	print(current_user_song_dicts)
	print(type(current_user_song_dicts))

	# RESPONSE
	return jsonify({
		'data': current_user_song_dicts,
		'message': f"Successfully found {len(current_user_song_dicts)} song(s)",
		'status': 200
	}), 200




### CREATE SONG ROUTE -- POST ###
@songs.route('/', methods=['POST'])
def create_song():

	payload = request.get_json()
	print(payload)

	add_song = models.Song.create(
		song_title=payload['song_title'],
		album_title=payload['album_title'],
		artist=payload['artist'],
		genre=payload['genre'],
		posted_by=current_user.id
	)
	print('- ' * 20)
	print('here is add_song')
	print(add_song)
	print('- ' * 20)
	print('here is add_song.__dict__')
	print(add_song.__dict__)
	print('- ' * 20)
	# print('here is dir(add_song)')
	# print(dir(add_song))

	song_dict = model_to_dict(add_song)
	song_dict['posted_by'].pop('password')

	# RESPONSE
	return jsonify(
		data=song_dict,
		message=f"Successfully added {song_dict['song_title']} by {song_dict['artist']}",
		status=201
	), 201



### DESTROY SONG ROUTE -- DELETE ###
@songs.route('/<id>', methods=['DELETE'])
@login_required
def delete_song(id):

	try:

		# RETRIEVE SONG
		song_to_delete = models.Song.get_by_id(id)

		# LOGIC TO SEE IF SONG BELONGS TO CURRENT USER
		if song_to_delete.posted_by.id == current_user.id:
			song_to_delete.delete_instance()

			# RESPONSE
			return jsonify(
				data={},
				message=f"Successfully deleted song with id of {id}",
				status=200
			), 200


		# LOGIC IF SONG DOES NOT BELONG TO CURRENT USER
		else:

			# RESPONSE
			return jsonify(
				data={
					'error': '403 Forbidden'
				},
				message='Song ID does not match user ID. Users can only delete their own songs',
				status=403
			), 403

	# LOGIC IF SONG DOES NOT EVEN EXIST
	except models.DoesNotExist:

		# RESPONSE
		return jsonify(
			data={
				'error': '404 Not Found'
			},
			message='There is no song with that ID',
			status=404
		), 404


### SONG UPDATE ROUTE -- PUT ###
@songs.route('/<id>', methods=['PUT'])
def update_song(id):

	payload = request.get_json()

	update_query = models.Song.update(
		song_title=payload['song_title'],
		album_title=payload['album_title'],
		artist=payload['artist'],
		genre=payload['genre'],
		posted_by=payload['posted_by']
	).where(models.Song.id == id)

	num_of_rows_updated = update_query.execute()

	updated_song = models.Song.get_by_id(id)
	updated_song_dict = model_to_dict(updated_song)


	# RESPONSE
	return jsonify(
		data=updated_song_dict,
		message=f"Successfully updated a song with the id of {id}",
		status=200
	), 200