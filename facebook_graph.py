#%%
from flask import render_template
import json
from networkx.readwrite import json_graph
import networkx as nx
import numpy as np
import pandas as pd
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import (Plot, Range1d, MultiLine, Circle, PanTool, HoverTool, BoxSelectTool, 
                            BoxZoomTool, ResetTool, WheelZoomTool, TapTool)
from bokeh.models import LinearColorMapper, ColumnDataSource, DataRange, GraphRenderer
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges, EdgesAndLinkedNodes, NodesOnly
from bokeh.models import BoxAnnotation, Annotation, Selection, TextInput
from bokeh.layouts import widgetbox
from bokeh.models.callbacks import CustomJS
from bokeh.palettes import Purples9, Viridis256
from bokeh.embed import components
from bokeh.resources import CDN

def fb_graph():

    with open('facebook.json', 'r') as read_file:
        data = json.load(read_file)
    FB = nx.Graph(incoming_graph_data=data)
    degrees = FB.degree()
    nodes = FB.nodes()

    eigenv = nx.eigenvector_centrality(FB, weight=None)
    between = nx.betweenness_centrality(FB, weight=None)

    node_color = {k:v for k, v  in FB.degree()}
    node_size = {k:.1*v for k,v in FB.degree()} 
    nx.set_node_attributes(FB, node_color, 'node_color')
    nx.set_node_attributes(FB, node_size, 'node_size')
    mapper = LinearColorMapper(palette=Viridis256, low=256, high=0)
    connections = list(node_color.values())
    eigenv = list(eigenv.values())
    between = list(between.values())

    source = ColumnDataSource(pd.DataFrame.from_dict({k:v for k,v in FB.nodes(data=True)},orient='index'))
    source.add(connections, "connections")
    source.add(eigenv, "eigenv")
    source.add(between, "between")

    boxcolor = BoxAnnotation(fill_color='white', line_color='black')

    plot_option = {
    'background_fill_color': 'gray',
    'background_fill_alpha': .5,
    'tools': [PanTool(), WheelZoomTool(), TapTool(), BoxZoomTool(overlay=boxcolor), BoxSelectTool(overlay=boxcolor), ResetTool()],
    'x_range': Range1d(-1,1), 
    'y_range': Range1d(-1,1),
    'plot_width': 800,
    'plot_height': 800,
    }

    plot = figure(**plot_option, x_axis_location=None, y_axis_location=None, output_backend="webgl")
    plot.title.text = "Facebook Graph"
    graph = from_networkx(FB, nx.spring_layout)
    graph.node_renderer.data_source = source
    graph.node_renderer.glyph = Circle(name="Node", size='node_size', fill_color={'field': 'node_color', 'transform': mapper})
    graph.edge_renderer.glyph = MultiLine(line_width=.5)
    graph.edge_renderer.selection_glyph = MultiLine(line_color='white', line_width=1)
    plot.add_tools(HoverTool(name="Node", tooltips=[('Node', '$index'), 
                            ('Connections', '@connections'), ('Eigen Value', '@eigenv{.000000}'), ('Betweenness', '@between{.000000}'), 
                            ]))
    graph.selection_policy = NodesAndLinkedEdges()

    #4038 total nodes

    plot.renderers.append(graph)
    script, div = components(plot)
    cdn_js = CDN.js_files
    cdn_css = CDN.css_files

    return plot

if __name__ == '__main__':
    plot = fb_graph()
    output_file("networkx_graph.html")
    show(plot)
