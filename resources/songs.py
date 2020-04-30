import models

from flask import Blueprint, request

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
	print(add_song)

	return 'you hit the song create route - check terminal'