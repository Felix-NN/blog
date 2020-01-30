from bs4 import BeautifulSoup
import requests
import csv
import re
from app import db
from app.models import Song, Answer

def source_check(src):
    if src.find('div', class_='embed-placeholder youtube-placeholder'):
        for item in src.find_all(attrs={"data-id": True}):
            data_id = []
            data_id.append(item['data-id'])
            data_id.append(1)
            return data_id
    elif src.find('iframe'):
        for item in src.find_all(attrs={"title": True}):
            data_id = []
            title = item['title']
            data_id.append(title.split(' ')[2])
            data_id.append(2)
            return data_id

def time_check(src):
    times = []
    if src.find_all(text=re.compile('and throughout')):
        times.append(1)
    else:
        times.append(0)
    for item in src.find_all(attrs={"data-timings": True}):
        data_times = item['data-timings']
        data_times = data_times.split(',')
        times.append(data_times)
    return times


url = 'https://www.whosampled.com/sample/'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}

with open('song_number.csv', mode='r') as csv_file:
    readcsv = csv.reader(csv_file, delimiter=',')
    for row in readcsv:
        full = row[0].split('_')
        samp_full = full[0].split('-')
        ans_full = full[1].split('-')
        samp_num = row[1]
        samp_art = samp_full[0]
        samp_art = samp_art.strip()
        samp_song = samp_full[1]
        samp_song = samp_song.strip()
        ans_art = ans_full[0]
        ans_art = ans_art.strip()
        ans_song = ans_full[1]
        ans_song = ans_song.strip()

        source = requests.get(url + str(samp_num), headers=headers).text
        soup = BeautifulSoup(source, 'lxml')

        section = soup.find('section')

        sample_html = section.find_all('div', class_='sample-embed')
        sample_1 = sample_html[0]
        sample_2 = sample_html[1]

        source_srctype_1 = source_check(sample_1)
        source_data_1 = source_srctype_1[0]
        src_type_1 = source_srctype_1[1]

        source_srctype_2 = source_check(sample_2)
        source_data_2 = source_srctype_2[0]
        src_type_2 = source_srctype_2[1]


        sample_times = section.find_all('div', class_='sample-timings')
        time_1 = sample_times[0]
        time_2 = sample_times[1]

        throughout_times_1 = time_check(time_1)
        throughout_1 = throughout_times_1[0]
        times_1 = throughout_times_1[1]

        throughout_times_2 = time_check(time_2)
        throughout_2 = throughout_times_2[0]
        times_2 = throughout_times_2[1]

        times_1 = ','.join(map(str, times_1))
        times_2 = ','.join(map(str, times_2)) 

        song_1 = Song(artist=samp_art, 
                    song_name=samp_song, 
                    source=source_data_1, 
                    source_type=src_type_1, 
                    times=times_1, 
                    throughout=throughout_1)

        db.session.add(song_1)

        song_2 = Answer(artist=ans_art, 
                    song_name=ans_song, 
                    source=source_data_2, 
                    source_type=src_type_2, 
                    times=times_2, 
                    throughout=throughout_2)

        db.session.add(song_2)

        song_1.answer.append(song_2)

        db.session.commit()