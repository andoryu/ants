import json

from graphviz import Digraph

ant_spec = json.load(open("../sample_ant_genome.json"))

dot = Digraph(comment=ant_spec['id'], format="svg", engine="dot")

# write out the basic nodes - including actions
for i, gene in enumerate(ant_spec['genes']):
    node_name  = 'state_{0:02}'.format(i)
    node_label = '{0:02}: {1}'.format(i, gene['action'])
    dot.node(node_name, node_label)

# write out the links labelling with view bit field
for i, gene in enumerate(ant_spec['genes']):
    source = "state_{:02}".format(i)

    for j, transition in enumerate(gene['transitions']):
        dest = "state_{:02}".format(transition)
        edge_label = "{:03b}".format(j)

        dot.edge(source, dest, label=edge_label)


svg = dot.pipe()
#dot.render()
