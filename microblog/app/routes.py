from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Myrtle'}
    posts = [
        {
            'author': {'username':'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username':'Sarah'},
            'body': 'Beautiful day in Seattle!'
        },
        {
            'author': {'username':'Lori'},
            'body': 'Beautiful day in Kalispell!'
        }
    ]
    return render_template('index.html', title= 'Home', user=user, posts=posts)
