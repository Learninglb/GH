import os
from datetime import datetime
from flask import render_template, flash, request, redirect, jsonify, make_response
from flask import send_from_directory, abort, session, url_for
from werkzeug.utils import secure_filename
from app import app


@app.route('/')
@app.route('/index')
def index():

    print(f"Flask ENV is set to: {app.config['ENV']}")
    return render_template('public/index.html', title='Home')


def allowed_file(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["FILES_ALLOWED"]:
        return True
    else:
        return False

def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["IMAGES_ALLOWED"]:
        return True
    else:
        return False

def allowed_file_filesize(filesize):

    if int(filesize) <= app.config["MAX_FILE_FILESIZE"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


@app.route('/jinja')
def jinja():

    my_name = "Lori"
    age = 17
    langs = ['English', 'German', 'Italian']
    friends = {
        'Charles': 44,
        'Clifford': 44,
        'Ethan': 14
    }
    colors = ('Red', 'Blue')
    cool = True

    class GitRemote:
        def __init__(self, name, description, url):
            self.name = name
            self.description = description
            self.url = url

        def pull(self):
            return f"Pulling repo {self.name}"

        def clone(self):
            return f"Cloning into {self.url}"

    my_remote = GitRemote(
        name="Flask Jinja",
        description="Template design",
        url="https://github"
    )

    def repeat(x, qty):
        return x * qty

    date = datetime.utcnow()

    my_html = "<h1>This is some HTML</h1>"

    suspicious = "<script>alert('NEVER TRUST USER INPUT!')</script>"

    return render_template(
        'public/jinja.html', my_name=my_name, age=age,
        langs=langs, friends=friends, colors=colors, cool=cool, GitRemote=GitRemote,
        repeat=repeat, my_remote=my_remote, date=date, my_html=my_html, suspicious=suspicious)


@app.route('/upload_csv', methods=["GET", "POST"])
def upload_csv():
    if request.method == "POST":

        if request.files:
            if "filesize" in request.cookies:

                if not allowed_file_filesize(request.cookies["filesize"]):
                    flash("Filesize exceeded maximum limit")
                    return redirect(request.url)
                    #return redirect(request.url)

                text = request.files['text']

                if text.filename == "":
                    flash("File must have a name.")
                    return redirect(request.url)
                    #return redirect(request.url)

                if not allowed_file(text.filename):
                    flash("That file extension is not allowed.")
                    return redirect(request.url)
                    #return redirect(request.url)
                else:
                    filename = secure_filename(text.filename)
                    text.save(os.path.join(app.config["FILE_UPLOAD"], filename))
                    flash("File saved.")
                    return redirect(request.url)
                    # ReadAndCreateFromCSV.py(filename)

    return render_template('public/upload_csv.html', title='Upload CSV')

@app.route('/upload_img', methods=["GET", "POST"])
def upload_img():
    if request.method == "POST":

        if request.files:
            if "filesize" in request.cookies:

                if not allowed_image_filesize(request.cookies["filesize"]):
                    flash("Image size exceeded maximum limit")
                    return redirect(request.url)               

                image = request.files['image']

                if image.filename == "":
                    flash("File must have a name.")
                    return redirect(request.url)

                if allowed_image(image.filename):
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config["IMAGE_UPLOAD"], filename))
                    flash("Image saved.")
                    return redirect(request.url)
                    # ReadAndCreateFromCSV.py(filename)
                else:
                    flash("That file extension is not allowed.")
                    return redirect(request.url)


    return render_template('public/upload_img.html')

@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%b %d %Y")


@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":

        req = request.form

        missing = list()

        for k, v in req.items():
            if v == "":
                missing.append(k)

        if missing:
            flash("Missing fields", "warning")
            return render_template("public/sign_up.html")

        password = req.get("password")

        if not len(password) >= 10:
            flash("Password must be at least 10 characters", "warning")
            return render_template("public/sign_up.html")

        flash("Account created!", "success")
        
    return render_template("public/sign_up.html")


users = {
    "mitsuhiko": {
        "name": "Armin Ronacher",
        "bio": "Creator of the Flask framework",
        "twitter_handle": "@mitsuhiko"
    },
    "Lori": {
        "username": "Lori",
        "email": "lblasing@flathead.coop",
        "password": "Flask",
        "bio": "Creator of fine art",
        "twitter_handle": "@GargoyleArt"
    },
    "gvanrossum": {
        "name": "Guido Van Rossum",
        "bio": "Creator of the Python programming language",
        "twitter_handle": "@gvanrossum"
    },
    "elonmusk": {
        "name": "Elon Musk",
        "bio": "technology entrepreneur, investor, and engineer, all around strange guy",
        "twitter_handle": "@elonmusk"
    }
}

@app.route("/json", methods=["POST"])
def json():

    # Validate the request body contains JSON
    if request.is_json:

        # Parse the JSON into a Python dictionary
        req = request.get_json()

        response = {
            "message": "JSON received!",
            "sender": req.get("name")
        }

        res = make_response(jsonify(response), 200)

        return res

    else:
        res = make_response(jsonify({"message": " Request was not JSON"}), 400)
        return res


@app.route("/guestbook")
def guestbook():
    return render_template("public/guestbook.html")


@app.route("/guestbook/create_entry", methods=["POST"])
def create_entry():

    req = request.get_json()

    print(req)

    res = make_response(jsonify(req), 200)
    return res


@app.route("/query")
def query():
    if request.args:

        # We have our query string nicely serialized as a Python dictionary
        args = request.args

        # We'll create a string to display the parameters & values
        serialized = ", ".join(f"{k}: {v}" for k, v in request.args.items())

        # Display the query string to the client in a different format
        return f"(Query) {serialized}", 200

    else:

        return "No query string received", 200

@app.route("/get_image/<image_name>")
def get_image(image_name):
    try:
        return send_from_directory(
            app.config["CLIENT_IMAGES"], filename=image_name, as_attachment=True
            )
    except FileNotFoundError:
        abort(404)
    
    return 'Thanks'

@app.route("/get_csv/<filename>")
def get_csv(filename):
    try:
        return send_from_directory(
            app.config["CLIENT_FILES"], filename=filename, as_attachment=True
            )
    except FileNotFoundError:
        abort(404)
    
    return 'Thanks'

@app.route("/get_dat/<path:path>")
def get_dat(path):
    try:
        return send_from_directory(
            app.config["CLIENT_DAT"], filename=path, as_attachment=True
            )
    except FileNotFoundError:
        abort(404)
    
    return 'Thanks'

# Build and find cookies
@app.route("/cookies")
def cookies():

    res = make_response("Cookies", 200)

    cookies = request.cookies
    flavor = cookies.get("flavor")
    choc_type = cookies.get("chocolate type")
    chewy = cookies.get("chewy")
 
    print(flavor, choc_type, chewy)

    res.set_cookie(
        "flavor", 
        value="chocolate chip",
        max_age=10,
        expires=None,
        path=request.path,
        domain=None,
        secure=False,
        httponly=False,
        samesite=None        
        )
    res.set_cookie("chocolate type", "dark")
    res.set_cookie("chewy", "yes")

    return res

# login with bad security
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        req = request.form

        username = req.get("username")
        password = req.get("password")

        if not username in users:
            flash("Username not found")
            return redirect(request.url)
        else:
            user = users[username]

        if not password == user["password"]:
            flash("Incorrect password")
            return redirect(request.url)
        else:
            session["USERNAME"] = user["username"]
            print("session username set")
            #return redirect(request.url)
            return redirect(url_for("profile"))

    return render_template("/public/login.html")
    
@app.route("/profile")
def profile():

    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user = users[username]
        return render_template("public/profile.html", user=user)
    else:
        print("No username found in session")
        return redirect(url_for("login"))

@app.route("/logout")
def sign_out():

    session.pop("USERNAME", None)

    return redirect(url_for("index"))
