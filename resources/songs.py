import models

from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user

songs = Blueprint('songs', 'songs')

### SONG INDEX ROUTE -- GET ###
@songs.route('/', methods=['GET'])
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
def delete_song(id):

	delete_query = models.Song.delete().where(models.Song.id == id)
	num_of_rows_deleted = delete_query.execute()
	print(num_of_rows_deleted)


	# RESPONSE
	return jsonify(
		data={},
		message=f"Successfully deleted {num_of_rows_deleted} song with id of {id}",
		status=200
	), 200



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