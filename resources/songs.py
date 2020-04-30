import models

from flask import Blueprint

songs = Blueprint('songs', 'songs')

@songs.route('/', methods=['GET'])
def test_songs():
	return 'songs resource working'