''' Custom error messages '''

from flask import render_template, request
from app import app

@app.errorhandler(404)
def not_found(error):
    ''' 404 error '''

    return render_template("public/404.html")

@app.errorhandler(500)
def server_error(error):
    ''' 500 error '''

    app.logger.error(f"Server error: {error}, route: {request.url}")
    return render_template("public/500.html")
