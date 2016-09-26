from flask import Flask, send_file
from flask import json, request
import networkx as nx
from networkx.readwrite import json_graph

app = Flask(__name__)

'''
random network algorithm
'''

@app.route("/")
def index():
    return send_file("templates/index.html")

@app.route("/generateGraph", methods=['POST'])
def generateGraph():
    try:
        action = request.json['userAction']
        print action
        G = eval('nx.'+action)
        data = json_graph.node_link_data(G)
        return json.dumps(data)
    except:
        return "error"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
