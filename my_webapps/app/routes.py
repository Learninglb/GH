import os
from flask import render_template, request, redirect
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

def allowed_file(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["FILES_ALLOWED"]:
        return True
    else:
        return False

@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":

        if request.files:
            text = request.files['text']

            if text.filename=="":
                print("File must have a name.")
                return redirect(request.url)
            
            if not allowed_file(text.filename):
                print("That file extension is not allowed.")
                return redirect(request.url)
            else:
                filename = secure_filename(text.filename)
                text.save(os.path.join(app.config["FILE_UPLOAD"], filename))

            print("file saved")
            return redirect(request.url)

    return render_template('upload.html', title='Upload')