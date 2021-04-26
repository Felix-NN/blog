from math import inf
from os import link
import json
import re
from flask import Flask, render_template, request, jsonify
from numpy.lib.utils import info
from app import app
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.embed import json_item

from bokeh.layouts import widgetbox
from bokeh.models import CustomJS, TextInput, Button

from facebook_graph import fb_graph
from ba_graph import bagraph
from ws_graph import wsgraph

from app import db
from app.models import Song, Answer

from sample_queries import random_song, next_song, prev_song, get_song, rand_ans

from yfinance_lookup import stock
from link_preview import *

import multiprocessing

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title = "Home")

@app.route('/graphs')
def graphs():
    ba_plot = bagraph(10, 5)
    ws_plot = wsgraph(10, 5, .5)
    
    plots = (ba_plot, ws_plot)
    script, div = components(plots)
    cdn_js = CDN.js_files
    cdn_css = CDN.css_files
  
    return render_template("network_graphs.html", 
    title = "Network Graphs",
    script = script,
    ba_div = div[0],
    ws_div = div[1],
    cdn_js = cdn_js,
    cdn_css = cdn_css)

@app.route('/_update_graph', methods=['GET', 'POST'])
def _update_graph():
    type_graph = request.form['graph']

    if type_graph == 'ba':
        ba_nodes = int(request.form['ba_nodes'])
        ba_edges = int(request.form['edges'])
        plot = bagraph(ba_nodes, ba_edges)
    elif type_graph == 'ws':
        ws_nodes = int(request.form['ws_nodes'])
        ws_n_conn = int(request.form['n_conn'])
        ws_prob = float(request.form['prob'])
        plot = wsgraph(ws_nodes, ws_n_conn, ws_prob)
    
    script, div = components(plot)
   
    return render_template("updated_graph.html", div = div, script = script)

@app.route('/references')
def references():
    return render_template("references.html", title = "References")

@app.route('/facebook_graph')
def facebook_graph():
    return render_template("facebook_graph.html")

@app.route('/restaurant')
def restaurant():
    return render_template("restaurant.html", title = "Restaurant Predictor")

@app.route('/sample')
def sample():
    song, answer, song_id = random_song()
    artist_1 = song.artist
    artist_2 = answer.artist
    song_name_1 = song.song_name
    song_name_2 = answer.song_name
    data_id_1 = song.source
    data_id_2 = answer.source
    source_type_1 = song.source_type
    source_type_2 = answer.source_type
    throughout_1 = song.throughout
    throughout_2 = answer.throughout
    times_1 = song.times.split(',')
    times_2 = answer.times.split(',')
    times_1 = [int(i) for i in times_1]
    times_2 = [int(i) for i in times_2]
    choices = rand_ans(song_id)
    full_ans = artist_2 + ' - ' + song_name_2
    choices.append(full_ans)
    song_info = {}
    count = 0
    while count <= 124:
        rel_song, extra = next_song(count)
        art = rel_song.artist
        song_nm = rel_song.song_name
        id_num = rel_song.id
        title = art + ' - ' + song_nm
        song_info[id_num] = title
        count = count + 1
        

    return render_template("sample.html", 
    title='Sample Quiz',
    artist_1 = artist_1,
    artist_2 = artist_2,
    song_name_1 = song_name_1,
    song_name_2 = song_name_2,
    data_id_1 = data_id_1, 
    data_id_2 = data_id_2,
    source_type_1 = source_type_1,
    source_type_2 = source_type_2,
    throughout_1 = throughout_1,
    throughout_2 = throughout_2,
    times_1 = times_1,
    times_2 = times_2,
    song_id = song_id,
    choices = json.dumps(choices),
    song_info = song_info)

@app.route('/_update_sample', methods=['GET', 'POST'])
def _update_sample():
    butt_choice = request.form['button']
    if butt_choice == 'random':
        song, answer, song_id = random_song()
    elif butt_choice == 'next':
        song_id = int(request.form['song_id'])
        song, answer = next_song(song_id)
        song_id = song_id + 1
    elif butt_choice == 'prev':
        song_id = int(request.form['song_id'])
        song, answer = prev_song(song_id)        
        song_id = song_id - 1
    elif butt_choice == 'get':
        song_id = int(request.form['song_id'])
        song, answer = get_song(song_id)
    
    artist_1 = song.artist
    artist_2 = answer.artist
    song_name_1 = song.song_name
    song_name_2 = answer.song_name
    data_id_1 = song.source
    data_id_2 = answer.source
    source_type_1 = song.source_type
    source_type_2 = answer.source_type
    throughout_1 = song.throughout
    throughout_2 = answer.throughout
    times_1 = song.times.split(',')
    times_2 = answer.times.split(',')
    times_1 = [int(i) for i in times_1]
    times_2 = [int(i) for i in times_2]
    choices = rand_ans(song_id)
    full_ans = artist_2 + ' - ' + song_name_2
    choices.append(full_ans)

    song_info = {}
    count = 0
    while count <= 124:
        rel_song, extra = next_song(count)
        art = rel_song.artist
        song_nm = rel_song.song_name
        id_num = rel_song.id
        title = art + ' - ' + song_nm
        song_info[id_num] = title
        count = count + 1

    return render_template("updated_sample.html", 
    artist_1 = artist_1,
    artist_2 = artist_2,
    song_name_1 = song_name_1,
    song_name_2 = song_name_2,
    data_id_1 = data_id_1, 
    data_id_2 = data_id_2,
    source_type_1 = source_type_1,
    source_type_2 = source_type_2,
    throughout_1 = throughout_1,
    throughout_2 = throughout_2,
    times_1 = times_1,
    times_2 = times_2,
    song_id = song_id,
    choices = json.dumps(choices),
    song_info = song_info)

@app.route('/stocks')
def stock_page():
    return render_template("stock.html", title='Stock History (React App)')

@app.route('/_update_stocks', methods=['GET', 'POST'])
def stock_update():
    company = request.get_json()
    lookup = stock()
    data = lookup.routine(company)
    return jsonify(data)

@app.route('/_link_prev', methods=['GET', 'POST'])
def get_link_prev():
    data = request.get_json()
    skip = ['nasdaq']
    data = list(filter(lambda x: not any(s in x.lower() for s in skip), data))
    pool = multiprocessing.Pool()
    info = pool.map(link_routine, data)
    pool.close()
    pool.join()
    info = list(filter(None, info))
    info = list(filter(None, ({key : val for key, val in sub.items() if val} for sub in info)))

    return jsonify(info)

    


if __name__=='__main__':
    app.run()