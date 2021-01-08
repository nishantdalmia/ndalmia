"""
Insta485 login view.

URLs include:
/accounts/login/
/accounts/logout/
"""
from flask import request, redirect, url_for, make_response, render_template
import insta485
from insta485.views.util import validate_password


@insta485.app.route('/accounts/login/', methods=['GET', 'POST'])
def login():
    """Display /accounts/login/ route."""
    if 'username' in request.cookies:
        return redirect(url_for('show_index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        validate_password(username, password)
        response = make_response(redirect(url_for('show_index')))
        response.set_cookie('username', username)
        return response

    return render_template('login.html')


@insta485.app.route('/accounts/logout/', methods=['POST'])
def logout():
    """Logout."""
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('username')
    return response
