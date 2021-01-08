"""
Insta485 login view.

URLs include:
/accounts/edit/
"""
import pathlib
import uuid
from flask import request, redirect, url_for, render_template, abort
import insta485
from insta485.views.util import validate_password, hash_password


@insta485.app.route('/accounts/edit/', methods=['GET', 'POST'])
def edit():
    """Display /accounts/edit/ route."""
    if 'username' in request.cookies:
        logname = request.cookies.get('username')

        if request.method == 'POST':
            if request.form.get('update') == 'submit':
                update_user(logname)

        connection = insta485.model.get_db()
        cur = connection.execute("SELECT * FROM users WHERE username = ?",
                                 (logname,))
        user = cur.fetchall()[0]
        user_img_url = "/uploads/" + user['filename']
        context = {"logname": logname,
                   "user_img_url": user_img_url,
                   "fullname": user['fullname'],
                   "email": user['email']}
        return render_template('edit.html', **context)

    return abort(404)


def update_user(logname):
    """Update user information."""
    fullname = request.form['fullname']
    email = request.form['email']

    connection = insta485.model.get_db()

    if request.files['file']:
        fileobj = request.files['file']
        filename = fileobj.filename

        uuid_basename = "{stem}{suffix}".format(
            stem=uuid.uuid4().hex,
            suffix=pathlib.Path(filename).suffix)
        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)

        cur = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (logname,))
        user = cur.fetchall()[0]
        cur = connection.execute(
            "UPDATE users "
            "SET fullname = ?, email = ?, filename = ? "
            "WHERE username = ?", (fullname, email, uuid_basename, logname,)
        )
        filename = user['filename']
        path = insta485.app.config["UPLOAD_FOLDER"]/filename
        path.unlink()
    else:
        cur = connection.execute("UPDATE users SET fullname = ?, email = ? "
                                 "WHERE username = ?",
                                 (fullname, email, logname,))


@insta485.app.route('/accounts/password/', methods=['GET', 'POST'])
def password():
    """Display /accounts/password/ route."""
    if 'username' in request.cookies:
        logname = request.cookies.get('username')

    if request.method == 'POST':
        if request.form.get('update_password') == 'submit':
            return update_user_password(logname)

    context = {"logname": logname, }
    return render_template('password.html', **context)


def update_user_password(logname):
    """Update user password."""
    passwrd = request.form['password']
    new_passwrd1 = request.form['new_password1']
    new_passwrd2 = request.form['new_password2']

    validate_password(logname, passwrd)
    if not new_passwrd1 == new_passwrd2:
        abort(401)

    connection = insta485.model.get_db()
    password_db_string = hash_password(new_passwrd1)
    connection.execute("UPDATE users SET password = ?",
                       (password_db_string,))

    return redirect(url_for('edit'))
