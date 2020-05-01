from app import app
from flask import render_template


@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html', title='Admin-Dashboard')

@app.route('/admin/profile')
def admin_profile():
    return render_template('admin/profile.html', title='Admin-Profile')
