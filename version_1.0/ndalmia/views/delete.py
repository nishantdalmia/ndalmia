"""
Insta485 login view.

URLs include:
/accounts/delete/
"""
from flask import request, redirect, url_for, \
                  make_response, render_template, abort
import insta485


@insta485.app.route('/accounts/delete/', methods=['GET', 'POST'])
def delete():
    """Display /accounts/delete/ route."""
    if 'username' in request.cookies:
        logname = request.cookies.get('username')

        if request.method == 'POST':
            if request.form.get('delete') == 'confirm delete account':
                connection = insta485.model.get_db()

                cur = connection.execute(
                    "SELECT filename FROM users WHERE username = ?",
                    (logname,))
                user_img = cur.fetchall()[0]
                cur = connection.execute(
                    "SELECT filename FROM posts WHERE owner = ?",
                    (logname,))
                posts = cur.fetchall()
                cur = connection.execute(
                    "DELETE FROM users WHERE username = ?",
                    (logname,))
                filename = user_img['filename']
                path = insta485.app.config["UPLOAD_FOLDER"]/filename
                path.unlink()
                for post in posts:
                    filename = post['filename']
                    path = insta485.app.config["UPLOAD_FOLDER"]/filename
                    path.unlink()

                response = make_response(redirect(url_for('create')))
                response.delete_cookie('username')
                return response

        context = {"logname": logname}
        return render_template('delete.html', **context)

    return abort(404)
