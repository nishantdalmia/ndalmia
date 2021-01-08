"""
Insta485 login view.

URLs include:
/accounts/create/
"""
import pathlib
import uuid
import hashlib
from flask import request, redirect, url_for, \
                  make_response, render_template, abort
import insta485
from insta485.views.util import validate


@insta485.app.route('/accounts/create/', methods=['GET', 'POST'])
def create():
    """Display /accounts/create/ route."""
    if 'username' in request.cookies:
        return redirect(url_for('edit'))

    if request.method == 'POST':
        validate(request.form['username'], 9)
        # if user_exists(request.form['username']):
        #     abort(409)
        if request.form['password'] == "":
            abort(400)
        return add_user()

    return render_template('create.html')


def add_user():
    """Add user."""
    username = request.form['username']
    email = request.form['email']
    fullname = request.form['fullname']
    password = request.form['password']

    fileobj = request.files['file']
    filename = fileobj.filename
    uuid_basename = "{stem}{suffix}".format(
        stem=uuid.uuid4().hex,
        suffix=pathlib.Path(filename).suffix)
    fileobj.save(insta485.app.config["UPLOAD_FOLDER"]/uuid_basename)

    salt = uuid.uuid4().hex
    hash_obj = hashlib.new('sha512')
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join(['sha512', salt, password_hash])

    # Connect to database
    connection = insta485.model.get_db()
    connection.execute(
        "INSERT INTO users(username, fullname, email, filename, password) "
        "VALUES(?, ?, ?, ?, ?)",
        (username, fullname, email, uuid_basename, password_db_string,))

    response = make_response(redirect(url_for('show_index')))
    response.set_cookie('username', username)
    return response
