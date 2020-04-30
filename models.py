from peewee import *
import datetime

from flask_login import UserMixin


DATABASE = SqliteDatabase('songs.sqlite')

class User(UserMixin, Model):
	name=CharField()
	username=CharField(unique=True)
	email=CharField(unique=True)
	password=CharField()

	class Meta:
		database = DATABASE


class Song(Model):
	song_title=CharField()
	album_title=CharField()
	artist=CharField()
	genre=CharField()
	posted_by=CharField()
	date_posted=DateField(default=datetime.date.today)

	class Meta:
		database = DATABASE


def initialize():
	DATABASE.connect()

	DATABASE.create_tables([User, Song], safe=True)
	print('Connected to database and created tables if they were not already there')

	DATABASE.close()