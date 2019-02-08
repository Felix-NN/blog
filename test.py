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
from bokeh.palettes import Purples9, Viridis256


user_node = 100
user_edge = 40
BA = nx.barabasi_albert_graph(int(user_node), int(user_edge)) 
degrees = BA.degree()
nodes = BA.nodes()


if user_node <= 10 or user_edge <= 10:
    multisize = 2
elif user_node <= 30 or user_edge <= 30:
    multisize = 1
elif user_node <= 50 or user_edge <= 50:
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
plot.title.text = "Barabasi-Albert Graph"
graph = from_networkx(BA, nx.spring_layout)
graph.node_renderer.data_source = source
graph.node_renderer.glyph = Circle(name="Node", size='node_size', fill_color={'field': 'node_color', 'transform': mapper})
graph.edge_renderer.selection_glyph = MultiLine(line_color='white', line_width=3)
plot.add_tools(HoverTool(name="Node", tooltips=[('Node', '$index'), 
                        ('Connections', '@connections'), ('Eigen Value', '@eigenv{.000000}'), ('Betweenness', '@between{.000000}'), 
                        ]))
graph.selection_policy = NodesAndLinkedEdges()
plot.renderers.append(graph)



print("Degrees: ", degrees)
print("\nNodes: ", nodes)
print("\nNode_color: ", node_color)
print("\nNode_size: ", node_size)
print("\nEdges: ", edges)

output_file("networkx_graph.html")
show(plot)



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
import bokeh.palettes as bp

#user_node = TextInput(title="Nodes:", value="# of Nodes for Graph")
#nodes_connect = TextInput(title="Connected:", value="How many nodes connected")
#prob = TextInput(title="Probability:", value="Probability of rewiring each edge")

#show(widgetbox([user_node, user_edge]))
user_node = 10
nodes_connect = 5
prob = .5
WS = nx.watts_strogatz_graph(int(user_node), int(nodes_connect), float(prob)) 
degrees = WS.degree()
nodes = WS.nodes()


if user_node <= 10 or nodes_connect <= 10:
    multisize = 2
elif user_node <= 30 or nodes_connect <= 30:
    multisize = 1
elif user_node <= 50 or nodes_connect <= 50:
    multisize = .5
else:
    multisize = .25


eigenv = nx.eigenvector_centrality(WS, weight=None)
between = nx.betweenness_centrality(WS, k=user_node, weight=None)
edges = list(nx.edges(WS))
edge_end = [edge[1] for edge in edges]

node_color = {k:v for k, v  in WS.degree()}
node_size = {k:multisize*v for k,v in WS.degree()} 
nx.set_node_attributes(WS, node_color, 'node_color')
nx.set_node_attributes(WS, node_size, 'node_size')
mapper = LinearColorMapper(palette=bp.Purples9, low=10, high=0)
connections = list(node_color.values())
eigenv = list(eigenv.values())
between = list(between.values())

source = ColumnDataSource(pd.DataFrame.from_dict({k:v for k,v in WS.nodes(data=True)},orient='index'))
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
plot.title.text = "Watts-Strogatz Graph"
graph = from_networkx(WS, nx.circular_layout)
graph.node_renderer.data_source = source
graph.node_renderer.glyph = Circle(name="Node", size='node_size', fill_color={'field': 'node_color', 'transform': mapper})
graph.edge_renderer.selection_glyph = MultiLine(line_color='white', line_width=3)
plot.add_tools(HoverTool(name="Node", tooltips=[('Node', '$index'), 
                        ('Connections', '@connections'), ('Eigen Value', '@eigenv{.000000}'), ('Betweenness', '@between{.000000}'), 
                        ]))
graph.selection_policy = NodesAndLinkedEdges()

plot.renderers.append(graph)

print("Degrees: ", degrees)
print("\nNodes: ", nodes)
print("\nNode_color: ", node_color)
print("\nNode_size: ", node_size)
print("\nEdges: ", edges)

output_file("networkx_graph.html")
show(plot)


#%%
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
from bokeh.palettes import Viridis256


with open('facebook.json', 'r') as read_file:
    data = json.load(read_file)
FB = nx.Graph(incoming_graph_data=data)
degrees = FB.degree()
nodes = FB.nodes()

"""
if user_node <= 10 or user_edge <= 10:
    multisize = 2
elif user_node <= 30 or user_edge <= 30:
    multisize = 1
elif user_node <= 50 or user_edge <= 50:
    multisize = .5
else:
    multisize = .25
"""

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
'output_backend': 'webgl'
}

plot = figure(**plot_option, x_axis_location=None, y_axis_location=None)
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
'''
print("Degrees: ", degrees)
print("\nNodes: ", nodes)
print("\nNode_color: ", node_color)
print("\nNode_size: ", node_size)
#print("\nEdges: ", edges)
'''
output_file("networkx_graph.html")
show(plot)

