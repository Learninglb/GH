from flask import render_template, request, redirect
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":

        if request.files:
            text = request.files['text']
            print (text)
            return redirect(request.url)

    return render_template('upload.html', title='Upload')