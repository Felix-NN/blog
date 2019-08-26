import json
from flask import Flask, render_template, request, jsonify
from app import app
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.embed import json_item

from bokeh.layouts import widgetbox
from bokeh.models import CustomJS, TextInput, Button

from facebook_graph import fb_graph
from ba_graph import bagraph
from ws_graph import wsgraph

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

if __name__=='__main__':
    app.run()