"""
ndalmia login view.

URLs include:
/login/
/logout/
"""
from flask import request, redirect, url_for, make_response, render_template
import ndalmia

@ndalmia.app.route('/login/', methods=['GET', 'POST'])
def login():
    """Display /login/ route."""
    if 'admin' in request.cookies:
        return redirect(url_for('show_index'))

    if request.method == 'POST':
        if request.form.get('admin_code') and request.form['admin_code'] == "$IAMADMIN$":
            response = make_response(redirect(url_for('show_index')))
            response.set_cookie('admin', 'admin')
            return response
        return redirect(url_for('show_index'))

    context = {'name': "Nishant Dalmia",
               'email': "ndalmia@umich.edu",
               'rmail': "ndalmia.recruit@gmail.com",
               'location': "Los Gatos, CA"}
    return render_template('login.html', **context)


@ndalmia.app.route('/logout/', methods=['POST'])
def logout():
    """Logout."""
    response = make_response(redirect(url_for('show_index')))
    response.delete_cookie('admin')
    return response
