import os
from flask import Flask, send_file, json, request, redirect, url_for
from werkzeug.utils import secure_filename

import networkx as nx
from networkx.readwrite import json_graph

UPLOAD_FOLDER = 'upload/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return send_file("templates/index.html")

@app.route("/generateGraph", methods=['POST'])
def generate_graph():
    try:
        action = request.json['userAction']
        print action
        G = eval('nx.'+action)
        data = json_graph.node_link_data(G)
        return json.dumps(data)
    except:
        return "error"

@app.route('/uploadGraph', methods=['POST'])
def upload_graph():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        gFile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print gFile
        return "success"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
