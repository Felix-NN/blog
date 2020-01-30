from app import db
from app.models import Song, Answer
import random

def random_song():
    rand = random.randint(1, 125)
    song = Song.query.get(rand)
    answer = Answer.query.get(rand)
    return song, answer, rand

def next_song(song_id):
    if song_id == 125:
        next_s = 1
    else:
        next_s = song_id + 1
    song = Song.query.get(next_s)
    answer = Answer.query.get(next_s)
    return song, answer

def prev_song(song_id):
    if song_id == 1:
        prev_s = 125
    else:
        prev_s = song_id - 1
    song = Song.query.get(prev_s)
    answer = Answer.query.get(prev_s)
    return song, answer

def get_song(song_id):
    song = Song.query.get(song_id)
    answer = Answer.query.get(song_id)
    return song, answer

def rand_ans(song_id):
    answer = Answer.query.get(song_id)
    options = answer.answers.split(',')
    options = random.sample(options, 3)
    return options
