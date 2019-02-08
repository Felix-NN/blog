from flask import Flask, render_template, request, jsonify
from app import app
from bokeh.resources import CDN
from bokeh.embed import components

from bokeh.layouts import widgetbox
from bokeh.models import CustomJS, TextInput, Button

from facebook_graph import fb_graph
from ba_graph import bagraph
from ws_graph import wsgraph

@app.route('/')
@app.route('/index')
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
    div1 = div[0],
    div2 = div[1],
    cdn_js = cdn_js,
    cdn_css = cdn_css)

@app.route('/_update_graph', methods=['POST'])
def _update_graph():
    ba_nodes = int(request.form('nodes'))
    ba_edges = int(request.form('edges'))
    print("ba_nodes = ", ba_nodes)
    print("ba_edges = ", ba_edges)
    ba_plot = bagraph(ba_nodes, ba_edges)
    script, div = components(ba_plot)

    return jsonify({'div' : div })

if __name__=='__main__':
    app.run()