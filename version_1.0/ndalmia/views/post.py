"""
Insta485 post view.

URLs include:
/p/<postid_url_slug>/
"""
from flask import request, redirect, url_for, \
                  render_template, abort
import insta485
from insta485.views.util import like_comment_post_request, \
                                add_post_details


@insta485.app.route('/p/<path:postid>/', methods=['GET', 'POST'])
def show_post(postid):
    """Display /p/<postid_url_slug>/ route."""
    if 'username' in request.cookies:
        logname = request.cookies.get('username')

        if request.method == 'POST':
            like_comment_post_request()
            if request.form.get('uncomment') == 'delete':
                remove_comment(logname)
            elif request.form.get('delete') == 'delete this post':
                return validate_and_delete_post(logname)

        return get_post_details(logname, postid)

    return redirect(url_for('login'))


def get_post_details(logname, postid):
    """Post Deatils Generator."""
    context = add_post_details(logname, postid)
    context.update({"logname": logname})

    return render_template('post.html', **context)


def validate_and_delete_post(logname):
    """Validate and Delete Post."""
    postid = request.form['postid']

    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT * FROM posts WHERE postid = ?",
        (postid,)
    )
    post = cur.fetchall()[0]
    if not post['owner'] == logname:
        abort(403)

    filename = post['filename']
    path = insta485.app.config["UPLOAD_FOLDER"]/filename
    path.unlink()
    cur = connection.execute(
        "DELETE FROM posts WHERE postid = ?",
        (postid,))

    user_path = "/u/" + logname + "/"
    return redirect(user_path)


def remove_comment(logname):
    """Remove comment from the database."""
    # Read request
    commentid = request.form['commentid']
    # Connect to database
    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT * FROM comments WHERE commentid = ?",
        (commentid,))
    if not cur.fetchall()[0]['owner'] == logname:
        abort(403)

    cur = connection.execute(
        "DELETE FROM comments WHERE commentid = ?",
        (commentid,))
