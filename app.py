import pathlib

from tinydb import TinyDB, where
from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename

import os

UPLOAD_FOLDER = os.getcwd() + "/functions"
ALLOWED_EXTENSIONS = {"py", "js"}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = TinyDB('database.json')

devicesDB = db.table('devices')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/device/<name>', methods=['GET', 'DELETE'])
def device(name):
    if request.method == 'GET':
        Device = devicesDB.search(where('name') == name)
        return render_template("device.html", device=Device[0]), 200
    elif request.method == 'DELETE':
        devicesDB.delete(where('name') == name)
        return {"message": "Device deleted"}, 200
    else:
        return "Request  not allowed", 405


@app.route('/function/upload/<dname>', methods=['POST'])
def upload_function(dname):
    if request.method == 'POST':
        if not pathlib.Path.exists(dname):
            os.mkdir(dname)
        else:
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('uploaded_file',
                                        filename=filename))
        return {"message": "Function created"}, 201
    else:
        return {"message": "Wrong method"}, 400


@app.route('/', methods=['GET', 'POST'])
def devices():
    if request.method == 'GET':
        return render_template("devices.html", devices=devicesDB.all()), 200
    elif request.method == 'POST':
        content = request.get_json()
        if devicesDB.search(where('name') == content['name']) is not None:
            return {"message": "Device already created"}, 200
        devicesDB.insert(content)
        return {"message": "Device created"}, 201


if __name__ == "__main__":
    app.run('0.0.0.0', 8080)
