#%%
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
from bokeh.palettes import Purples9
from bokeh.embed import components
from bokeh.resources import CDN


def bagraph(user_node, user_edge):
    BA = nx.barabasi_albert_graph(int(user_node), int(user_edge)) 
    degrees = BA.degree()
    nodes = BA.nodes()

    if user_node <= 10 and user_edge <= 10:
        multisize = 2
    elif user_node <= 20 and user_edge <= 20:
        multisize = 1.5
    elif user_node <= 30 and user_edge <= 30:
        multisize = 1
    elif user_node <= 50 and user_edge <= 50:
        multisize = .5
    else:
        multisize = .25


    eigenv = nx.eigenvector_centrality(BA, weight=None)
    between = nx.betweenness_centrality(BA, k=user_node, weight=None)
    edges = list(nx.edges(BA))
    edge_end = [edge[1] for edge in edges]

    node_color = {k:v for k, v  in BA.degree()}
    node_size = {k:multisize*v for k,v in BA.degree()} 
    nx.set_node_attributes(BA, node_color, 'node_color')
    nx.set_node_attributes(BA, node_size, 'node_size')
    mapper = LinearColorMapper(palette=Purples9, low=user_node, high=0)
    connections = list(node_color.values())
    eigenv = list(eigenv.values())
    between = list(between.values())

    source = ColumnDataSource(pd.DataFrame.from_dict({k:v for k,v in BA.nodes(data=True)},orient='index'))
    source.add(connections, "connections")
    source.add(eigenv, "eigenv")
    source.add(between, "between")

    boxcolor = BoxAnnotation(fill_color='white', line_color='black')

    plot_option = {
    'background_fill_color': 'gray',
    'background_fill_alpha': .5,
    'tools': [PanTool(), WheelZoomTool(), TapTool(), BoxZoomTool(overlay=boxcolor), BoxSelectTool(overlay=boxcolor), ResetTool()],
    'x_range': Range1d(-2,2), 
    'y_range': Range1d(-2,2),
    }

    plot = figure(**plot_option, x_axis_location=None, y_axis_location=None)
    plot.title.text = "Barabási-Albert Graph"
    graph = from_networkx(BA, nx.spring_layout)
    graph.node_renderer.data_source = source
    graph.node_renderer.glyph = Circle(name="Node", size='node_size', fill_color={'field': 'node_color', 'transform': mapper})
    graph.edge_renderer.selection_glyph = MultiLine(line_color='white', line_width=3)
    plot.add_tools(HoverTool(name="Node", tooltips=[('Node', '$index'), 
                            ('Connections', '@connections'), ('Eigen Value', '@eigenv{.000000}'), ('Betweenness', '@between{.000000}'), 
                            ]))
    graph.selection_policy = NodesAndLinkedEdges()
    plot.toolbar.active_scroll = plot.select_one(WheelZoomTool)
    plot.toolbar.autohide = True
    
    plot.renderers.append(graph)
    return plot
    
if __name__ == '__main__':
    user_node = 100
    user_edge = 40
    plot = bagraph(user_node, user_edge)
    output_file("networkx_graph.html")
    show(plot)
