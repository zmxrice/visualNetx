import os
import time
from flask import Flask, send_file, json, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

import networkx as nx
from networkx.readwrite import json_graph

UPLOAD_FOLDER = 'upload/'
GENERATE_FOLDER = 'generate/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GENERATE_FOLDER'] = GENERATE_FOLDER
app.config['GENERATED_GRAPH'] = None

@app.route("/")
def index():
    return send_file("templates/index.html")

@app.route("/generateGraph", methods=['POST'])
def generate_graph():
    try:
        action = request.json['userAction']
        G = eval('nx.'+action)
        app.config['GENERATED_GRAPH'] = G
        data = json_graph.node_link_data(G)
        return json.dumps(data)
    except:
        return "error"

@app.route('/uploadGraph', methods=['POST'])
def upload_graph():
    if 'file' not in request.files:
        flash('No file part')
        return "error"
    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return "error"
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        gFile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print gFile
        return "success"

@app.route('/exportGraph', methods=['POST'])
def export_graph():
    if app.config['GENERATED_GRAPH']:
        requestFormat = request.json['fmat']
        filename = str(int(time.time()))
        #choose graph generator based on user selection
        if requestFormat == "adjlist":
            filename += ".adjlist"
            fPath = os.path.join(app.config['GENERATE_FOLDER'], filename)
            fh=open(fPath,'wb')
            nx.write_adjlist(app.config['GENERATED_GRAPH'], fh)
            fh.close()

        elif requestFormat == "edgelist":
            filename += ".edgelist"
            fPath = os.path.join(app.config['GENERATE_FOLDER'], filename)
            fh=open(fPath,'wb')
            nx.write_edgelist(app.config['GENERATED_GRAPH'], fh)
            fh.close()

        return url_for('generated_file',filename=filename)
    else:
        return "error"


@app.route('/generated/<filename>')
def generated_file(filename):
    return send_from_directory(app.config['GENERATE_FOLDER'],filename, as_attachment=True)



if __name__ == "__main__":
    app.run(host='0.0.0.0')
