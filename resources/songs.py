import models

from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict

songs = Blueprint('songs', 'songs')

@songs.route('/', methods=['GET'])
def songs_index():
	return 'songs resource working'

@songs.route('/', methods=['POST'])
def create_song():

	payload = request.get_json()
	print(payload)

	add_song = models.Song.create(
		song_title=payload['song_title'],
		album_title=payload['album_title'],
		artist=payload['artist'],
		genre=payload['genre'],
		posted_by=['posted_by']
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

	# RESPONSE
	return jsonify(
		data=song_dict,
		message=f"Successfully added {song_dict['song_title']} by {song_dict['artist']}",
		status=201
	), 201