from googlesearch import search
import random
import csv
import time


domain = ['whosampled.com']

def g_search(song, rand):
    for res in search(song, tld='com', lang='en', domains=domain, num=1, pause=rand, stop=1): 
        res = res.split('/')
        song_dict.update({song : res[4]})

songs = []
song_dict = {}

with open('Songs.txt', 'r') as song_list:
    for song in song_list:
        songs.append(song.rstrip('\n'))

for que in songs[83]:
    rand = random.randrange(150, 300)
    rand = float(rand)
    rand = rand/10
    try:
        g_search(que, rand)
    except:
        print('Error! Saving songs done so far')
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print(current_time)
        break

w = csv.writer(open('song_number.csv', 'a', newline=''))
for key, val in song_dict.items():
    w.writerow([key, val])
    