from typing import NoReturn
from tinydb import TinyDB, where, Query
from tinydb.operations import add, set

from flask import Flask, request, render_template, redirect, url_for, make_response, flash
from werkzeug.utils import secure_filename

import os
import pathlib
from datetime import datetime

from os import listdir
from os.path import isfile, join


UPLOAD_FOLDER = os.getcwd() + "/scripts"
ALLOWED_EXTENSIONS = ["py"]

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'W-27$UU_#9B$74Nb'

db = TinyDB('database.json')

devicesDB = db.table('devices')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def updateScripts(args):
    def transform(name):
        Device = devicesDB.search(where('name') == name)
        Device['scripts'].append(args)
        devicesDB.update(set(Device),where('name') == name)

    return transform

@app.route('/device/<name>', methods=['GET', 'PUT', 'DELETE'])
def device(name):

    if request.method == 'GET':
        Device = devicesDB.search(where('name') == name)
        resp = make_response(render_template("device.html", device=Device[0]))
        resp.set_cookie("device", name)
        return resp

    if request.method == 'PUT':
        updatedValues = request.get_json()
        print(updatedValues)
        devicesDB.update(set(updatedValues), where('name') == name)
        return redirect('/', code=302) 

    if request.method == 'DELETE':
        devicesDB.remove(where('name') == name)
        return redirect('/', code=302)


@app.route('/script/upload', methods=['GET', 'POST'])
def upload_function():
    name = request.cookies.get("device")

    if request.method == 'GET':
        return render_template('upload_script.html')

    if request.method == 'POST':

        uploadTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        if not pathlib.Path(os.path.join(UPLOAD_FOLDER, name)).exists():
            os.mkdir(os.path.join(UPLOAD_FOLDER, name))
            # check if the post request has the file part
            if 'file' not in request.files:
                return redirect('/scripts', code=302)
                
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                return redirect('/scripts', code=302)

            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, name, filename))
                scriptData = {'scriptName': filename, 'uploadTime': uploadTime}    
                devicesDB.update(add("scripts", scriptData), where('name') == name)
                return redirect('/device/' + name, code=302)

            else:
               return redirect('/scripts', code=302)

        else:
            # check if the post request has the file part
            if 'file' not in request.files:
                return redirect('/scripts', code=302)
                
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                return redirect('/scripts', code=302)

            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, name, filename))
                scriptData = {'scriptName': filename, 'uploadTime': uploadTime}
                print(scriptData) 
                print(devicesDB.search(where('name') == name)[0]['scripts'])   
                devicesDB.update(add("scripts", scriptData), where('name') == name)
                return redirect('/scripts', code=302)

            else:
               return redirect('/scripts', code=302) 


@app.route('/scripts', methods=['GET', 'POST'])
def list_scripts():
    name = request.cookies.get("device")

    if request.method == 'GET':

        if devicesDB.search(where('name') == name) is None:
            flash('Device not found', 'error')
            return redirect('/', code=302)

        else:
            try:
                script_path = join(UPLOAD_FOLDER, name)
                uploadTimes = devicesDB.search(where('name') == name)[0]['scripts']['uploadTime']
                #print(uploadDates)
                scripts = [file for file in listdir(script_path) if isfile(join(script_path, file))]
                return render_template("scripts.html", scripts=scripts, uploadTimes = uploadTimes)
            except:
                flash('No files uploaded', 'warning')
                return redirect('/script/upload', code=302)

    if request.method == 'POST':
        return redirect('/', code=302)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html", devices=devicesDB.all())

    if request.method == 'POST':

        newDevice = {
            "name": request.form['name'],
            "type": request.form['type'],
            "ip": request.form['ip'],
            "scripts": []
        }

        if len(devicesDB.search(where('name') == newDevice['name'])) != 0:
            flash('Device already exists', 'error')
            return redirect('/', code=302)

        else:
            devicesDB.insert(newDevice)
            flash('Device created', 'success')
            return redirect('/', code=302)


if __name__ == "__main__":
    app.run(port=8080)
