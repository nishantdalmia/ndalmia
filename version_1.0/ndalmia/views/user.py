"""
Insta485 user page view.

URLs include:
/u/<user_url_slug>/
"""
import pathlib
import uuid
from flask import request, redirect, url_for, render_template
import insta485
from insta485.views.util import validate, follow, unfollow


@insta485.app.route('/u/<path:username>/', methods=['GET', 'POST'])
def show_user_page(username):
    """Display /u/<user_url_slug>/ route."""
    if 'username' in request.cookies:
        logname = request.cookies.get('username')

        validate(username)
        if request.method == 'POST':
            if request.form.get('unfollow') == 'unfollow':
                unfollow(logname, username)
            elif request.form.get('follow') == 'follow':
                follow(logname, username)
            elif request.form.get('create_post') == 'upload new post':
                upload_post(logname)

        return get_user_profile(logname, username)

    return redirect(url_for('login'))


def get_user_profile(logname, username):
    """Generate User Profile."""
    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    cur = connection.execute("SELECT fullname FROM users WHERE username = ?",
                             (username,))
    user = cur.fetchall()[0]

    cur = connection.execute("SELECT * FROM following WHERE username1 = ? "
                             "AND username2 = ?", (logname, username,))
    logname_follows_username = len(cur.fetchall()) == 1

    cur = connection.execute("SELECT postid, filename FROM posts "
                             "WHERE owner = ?", (username,))
    posts = cur.fetchall()
    posts_details = get_posts(posts)
    total_posts = len(posts_details)

    cur = connection.execute("SELECT * FROM following "
                             "WHERE username1 = ?", (username,))
    following = len(cur.fetchall())

    cur = connection.execute("SELECT * FROM following "
                             "WHERE username2 = ?", (username,))
    followers = len(cur.fetchall())
    # Add database info to context
    context = {"logname": logname,
               "username": username,
               "logname_follows_username": logname_follows_username,
               "fullname": user['fullname'],
               "following": following,
               "followers": followers,
               "total_posts": total_posts,
               "posts": posts_details}
    return render_template('user.html', **context)


def get_posts(posts):
    """Generate Post Details."""
    new_posts = list()
    for post in posts:
        img_url = "/uploads/" + post['filename']
        new_post = {"postid": post['postid'],
                    "img_url": img_url}
        new_posts.append(new_post)

    return new_posts


def upload_post(owner):
    """Upload Post."""
    # Unpack flask object
    fileobj = request.files['file']
    print(fileobj)
    filename = fileobj.filename

    # Compute base name (filename without directory).  We use a UUID to avoid
    # clashes with existing files, and ensure that the name is compatible with
    # the filesystem.
    uuid_basename = "{stem}{suffix}".format(
        stem=uuid.uuid4().hex,
        suffix=pathlib.Path(filename).suffix)

    # Save to disk
    path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)
    # Connect to database
    connection = insta485.model.get_db()
    connection.execute("INSERT INTO posts(filename, owner) VALUES(?, ?)",
                       (uuid_basename, owner,))
