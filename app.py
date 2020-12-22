from tinydb import TinyDB, where
from flask import Flask, request, render_template

app = Flask(__name__)
db = TinyDB('database.json')

devicesDB = db.table('devices')


@app.route('/device/<name>', methods=['GET', 'POST', 'DELETE'])
def device(name):
    if request.method == 'GET':
        Device = devicesDB.search(where('name') == name)
        return render_template("device.html", device=Device[0]), 200
    elif request.method == 'POST':
        data = request.get_json()
        return {"message": "Device created"}, 201
    elif request.method == 'DELETE':

        return {"message": "Device deleted"}, 200
    else:
        return "Request  not allowed", 405


@app.route('/function/<devicename>/<functionname>', methods=['GET', 'POST', 'DELETE'])
def function(devicename, functionname):
    if request.method == 'GET':
        return render_template('function.html'), 200
    elif request.method == 'POST':
        return "Function created", 201


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
