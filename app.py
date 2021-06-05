from typing import NoReturn
from tinydb import TinyDB, where

from flask import Flask, request, render_template, redirect, url_for, make_response, flash
from werkzeug.utils import secure_filename

import os
import pathlib
import subprocess
import psutil

from os import listdir
from os.path import isfile, join


UPLOAD_FOLDER = os.getcwd() + "/functions"
ALLOWED_EXTENSIONS = ["py"]

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'W-27$UU_#9B$74Nb'

db = TinyDB('database.json')

devicesDB = db.table('devices')


class Script():

    def __init__(self, filepath):
        self.filepath = filepath
        self.status = {"message" : "", "code" : 0}
        self.p = None
        return


    def getStatus(self):

        if not os.path.exists(self.filepath):
            self.status['message'] = "File not found"
            self.status['code'] = 1

        elif not self.filepath.split(".")[1] == "py":
            self.status['message'] = "Not supported filetype"
            self.status['code'] = 2

        elif self.p.returncode == 0:
            self.status['message'] = "Script executed"
            self.status['code'] = 3

        elif self.p.returncode == 1:
            self.status['message'] = "Script terminated"
            self.status['code'] = 4

        else:
            self.status['message'] = "Script running"
            self.status['code'] = 0

        return self.status


    def run(self):
        self.p = subprocess.Popen(["python", self.filepath], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        return


    def kill(self):
        self.p.kill()
        return


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/device/<name>', methods=['GET', 'PUT', 'DELETE'])
def device(name):

    if request.method == 'GET':
        Device = devicesDB.search(where('name') == name)
        resp = make_response(render_template("device.html", device=Device[0]))
        resp.set_cookie("device", name)
        return resp

    if request.method == 'PUT':
        updatedValues = request.get_json()
        devicesDB.update(set(updatedValues), where('name') == name)
        flash('Device edited', 'success')
        return redirect('/'), 308

    if request.method == 'DELETE':
        devicesDB.remove(where('name') == name)
        flash('Device deleted', 'success')
        return redirect('/'), 308


@app.route('/function/upload', methods=['GET', 'POST'])
def upload_function():
    name = request.cookies.get("device")

    if request.method == 'GET':
        return render_template('upload_function.html')

    if request.method == 'POST':

        if not pathlib.Path(os.path.join(UPLOAD_FOLDER, name)).exists():
            os.mkdir(os.path.join(UPLOAD_FOLDER, name))
            flash('Folder created. Please reupload', 'warning')
            return redirect('/function/upload'), 308

        else:
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part', 'warning')
                return redirect('/functions'), 308
                
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file', 'warning')
                return redirect('/functions'), 308

            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, name, filename))
                return redirect('/functions'), 308


@app.route('/functions')
def list_functions():
    name = request.cookies.get("device")

    if devicesDB.search(where('name') == name) is None:
        flash('Device not found', 'error')
        return redirect('/'), 308

    else:
        try:
            script_path = join(UPLOAD_FOLDER, name)
            scripts = [file for file in listdir(script_path) if isfile(join(script_path, file))]
            return render_template("functions.html", scripts=scripts)
        except:
            flash('No files uploaded', 'warning')
            return redirect('/function/upload')


@app.route('/function/run/<filename>')
def run_function(filename):
    name = request.cookies.get("device")

    if devicesDB.search(where('name') == name) is None:
        flash('Device not found', 'error')
        return redirect('/'), 308

    else:
        """
        interpreter for python scripts
        """
        status = Script(join(UPLOAD_FOLDER, name, filename)).getStatus()

        return render_template('/')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("devices.html", devices=devicesDB.all())

    if request.method == 'POST':

        newDevice = {
            "name": request.form['name'],
            "type": request.form['type'],
            "ip": request.form['ip']
        }

        if len(devicesDB.search(where('name') == newDevice['name'])) != 0:
            flash('Device already exists', 'error')
            return redirect('/')

        elif not (all(newDevice.values())):
            flash('You need to fill the device information', 'error')
            return redirect('/')

        else:
            devicesDB.insert(newDevice)
            flash('Device created', 'success')
            return redirect('/')


if __name__ == "__main__":
    app.run(port=8080)
