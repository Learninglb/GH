''' Admin '''
from flask import render_template
from app import app



@app.route('/admin/dashboard')
def admin_dashboard():
    ''' Dashboard '''
    return render_template('admin/dashboard.html', title='Admin-Dashboard')

@app.route('/admin/profile')
def admin_profile():
    ''' Profile '''
    return render_template('admin/profile.html', title='Admin-Profile')
