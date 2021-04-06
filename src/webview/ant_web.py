import json

from flask import Flask
from flask import Markup
from flask import render_template
from flask import send_from_directory

from graphviz import Digraph


app = Flask(__name__, static_url_path='')

@app.route("/")
def main():
    return "This is the main page"

@app.route("/css/<path:path>")
def send_css(path):
    return send_from_directory('css', path)

@app.route("/test_svg")
def svg_test():
    map_test = json.load(open("../simple-map.json"))

    ant_spec = json.load(open("../sample_ant_genome.json"))
    ant_svg = convert_ant_to_json(ant_spec)

    return render_template('svg_test.html', map=map_test, ant_svg=Markup(ant_svg))



def convert_ant_to_json(ant_spec):

    dot = Digraph(comment=ant_spec['id'], format="svg", engine="dot")

    # write out the basic nodes - including actions
    for i, gene in enumerate(ant_spec['genes']):
        node_name  = 'state_{0:02}'.format(i)
        node_label = '{0:02}: {1}'.format(i, gene['action'])
        dot.node(node_name, label=node_label, id=node_name)

    # write out the links labelling with view bit field
    for i, gene in enumerate(ant_spec['genes']):
        source = "state_{:02}".format(i)

        for j, transition in enumerate(gene['transitions']):
            dest = "state_{:02}".format(transition)
            edge_label = "{:03b}".format(j)
            edge_id = "{}-{}".format(source,dest)

            dot.edge(source, dest, label=edge_label, id=edge_id)


    return dot.pipe().decode('UTF-8')
