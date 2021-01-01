from tinydb import TinyDB, where

from flask import Flask, request, render_template, redirect, url_for, make_response
from werkzeug.utils import secure_filename

import os
import pathlib

UPLOAD_FOLDER = os.getcwd() + "/functions"
ALLOWED_EXTENSIONS = {"py", "js"}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = TinyDB('database.json')

devicesDB = db.table('devices')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/device/<name>', methods=['GET', 'PUT', 'DELETE'])
def device(name):
    if request.method == 'GET':
        if devicesDB.search(where('name') == name) is None:
            return {"message": "No device found"}, 404

        Device = devicesDB.search(where('name') == name)
        resp = make_response(render_template("device.html", device=Device[0]))
        resp.set_cookie("device", name)
        return resp

    if request.method == 'PUT':
        updatedValues = request.get_json()
        print(updatedValues)
        devicesDB.update(set(updatedValues), where('name') == name)
        return redirect(url_for('/'))

    if request.method == 'DELETE':
        devicesDB.remove(where('name') == name)
        return redirect(url_for('/'))

    else:
        return "Request not allowed", 405


@app.route('/function/upload', methods=['POST'])
def upload_function():
    name = request.cookies.get("device")

    if request.method == 'POST':

        if not pathlib.Path(os.path.join(UPLOAD_FOLDER, name)).exists():
            os.mkdir(os.path.join(UPLOAD_FOLDER, name))
            return {"message": "Folder for functions created."}, 200

        else:
            print('2')
            # check if the post request has the file part
            if 'file' not in request.files:
                # flash('No file part')
                return redirect(url_for('list_functions'))
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                print('4')
                # flash('No selected file')
                return redirect(url_for('list_functions'))
            if file and allowed_file(file.filename):
                print('5')
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], name, filename))
                return redirect(url_for('list_functions'))

    else:
        return {"message": "Wrong method"}, 400


@app.route('/functions')
def list_functions():
    name = request.cookies.get("device")

    if devicesDB.search(where('name') == name) is None:
        return {"message": "No device found"}, 404

    else:
        from os import listdir
        from os.path import isfile, join
        script_path = join(UPLOAD_FOLDER, name)
        scripts = [f for f in listdir(script_path) if isfile(join(script_path, f))]
        return render_template("functions.html", scripts=scripts)


@app.route('/function/run')
def run_function():
    name = request.cookies.get("device")

    if devicesDB.search(where('name') == name) is None:
        return {"message": "No device found"}, 404

    else:
        """
        interpreter for python and js scripts
        """
        return {"message": "under construction"}, 200


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("devices.html", devices=devicesDB.all()), 200

    if request.method == 'POST':

        newDevice = {
            "name": request.form['name'],
            "type": request.form['type'],
            "ip": request.form['ip']
        }

        if len(devicesDB.search(where('name') == newDevice['name'])) != 0:
            return {"message": "Device already exists"}, 200

        else:
            devicesDB.insert(newDevice)
            return {"message": "Device created"}, 201


if __name__ == "__main__":
    app.run(port=8080)
