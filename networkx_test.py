import json
import requests
import networkx as nx
import matplotlib.pyplot as plt

personas = 'http://story-chronicles.herokuapp.com/storyobjects/'
target = requests.get(personas)
x = target.json()

story_objects = {}
labels = {}
node_colors = []

for character in x:
    name = character["name"]
    story = character["story"]
    c_type = character["c_type"]
    story_objects[name] = {}
    story_objects[name]['name'] = name
    story_objects[name]['story'] = story
    story_objects[name]['c_type'] = c_type
    story_objects[name]['to_relationships'] = []
    if character['c_type'] == "Character":
        story_objects[name]['node_shape'] = 'o'
        story_objects[name]['node_color'] = 'r'
    elif character['c_type'] == "Organization":
        story_objects[name]['node_shape'] = 'h'
        story_objects[name]['node_color'] = 'b'
    elif character['c_type'] == "Creature":
        story_objects[name]['node_shape'] = '^'
        story_objects[name]['node_color'] = 'g'
    elif character['c_type'] == "Force":
        story_objects[name]['node_shape'] = 'v'
        story_objects[name]['node_color'] = 'c'
    elif character['c_type'] == "Thing":
        story_objects[name]['node_shape'] = 's'
        story_objects[name]['node_color'] = 'y'

    for relationship in character["to_relationships"]:
        break_1 = relationship.find(">")
        break_2 = relationship.find(">>")
        break_3 = relationship.find("(")
        break_4 = relationship.find(")")
        break_5 = relationship.find("weight:")
        subject = relationship[0:break_1].strip()
        context = relationship[break_1+1:break_2].strip()
        target = relationship[break_2+2:break_3]
        weight = relationship[break_5+8:-1]
        story_objects[name]['to_relationships'].append([subject, context, target, weight])

G=nx.MultiDiGraph()

for sub in story_objects:
    s = story_objects[sub]
    if s['story'] == "http://story-chronicles.herokuapp.com/story/1/":
        G.add_node(s['name'], node_shape=s['node_shape'])
        labels[s['name']] = s['name']

        node_colors.append(s['node_color'])

        print("***", s['name'], "***", s['c_type'])
        print("details:", s['node_color'], s['node_shape'])
        for i in s['to_relationships']:
            print('target:', i[2])
            print('context:', i[1])
            print('weight:', i[3])
            G.add_edge(s['name'], i[0], label=i[2], weight=int(i[3]))
        print("")

node_shapes=nx.get_node_attributes(G, 'node_shape') # Latest attempt at getting this to work
node_shapes = [v for k,v in node_shapes.items()]

pos=nx.spring_layout(G)
G.degree(weight=weight)

nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_shape=node_shapes.pop(0)) # <--- This is where I'm having problems
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos, labels)

plt.show()
