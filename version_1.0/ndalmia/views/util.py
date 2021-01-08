"""
Insta485 Utility.

URLs include:
-None-

Only for utility purposes
"""
import uuid
import hashlib
from flask import request, abort
import arrow
import insta485


def validate(username, abort_type=4):
    """Validate username."""
    connection = insta485.model.get_db()

    cur = connection.execute("SELECT * FROM users WHERE username = ?",
                             (username,))
    user_exists = len(cur.fetchall()) == 1

    if abort_type == 9:
        if user_exists:
            abort(409)
    else:
        if not user_exists:
            abort(404)


def get_comments(postid):
    """Get the comments on a specified post in dict format."""
    # Connect to database
    connection = insta485.model.get_db()
    # Get comments
    cur = connection.execute(
        "SELECT * FROM comments WHERE postid = ?", (postid,))
    comments = [dict(row) for row in cur.fetchall()]
    return comments


def add_comment():
    """Add a new comment to the database."""
    # Read request
    username = request.cookies.get('username')
    postid = request.form['postid']
    text = request.form['text']
    # Connect to database
    connection = insta485.model.get_db()
    # Add new comment
    connection.execute(
        "INSERT INTO comments(owner, postid, text) VALUES (?, ?, ?)",
        (username, postid, text))


def like():
    """Add a like to the database."""
    # Read request
    username = request.cookies.get('username')
    postid = request.form['postid']
    # Connect to database
    connection = insta485.model.get_db()
    # Add new like
    connection.execute(
        "INSERT INTO likes(owner, postid) VALUES (?, ?)",
        (username, postid,))


def unlike():
    """Remove a like from the database."""
    # Read request
    username = request.cookies.get('username')
    postid = request.form['postid']
    # Connect to database
    connection = insta485.model.get_db()
    # Remove like
    connection.execute("DELETE FROM likes WHERE owner = ? AND postid = ?",
                       (username, postid,))


def follow(logname, username):
    """Follow."""
    # Connect to database
    connection = insta485.model.get_db()
    connection.execute("INSERT INTO following(username1, username2) "
                       "VALUES(?, ?)",
                       (logname, username,))


def unfollow(logname, username):
    """Unfollow."""
    # Connect to database
    connection = insta485.model.get_db()
    connection.execute("DELETE FROM following WHERE username1 = ? "
                       "AND username2 = ?",
                       (logname, username,))


def follow_post_request(logname):
    """Process follow/unfollow request."""
    if request.method == 'POST':
        if request.form.get('unfollow') == 'unfollow':
            unfollow(logname, request.form.get('username'))
        elif request.form.get('follow') == 'follow':
            follow(logname, request.form.get('username'))


def like_comment_post_request():
    """Process like/unlike/addcomment request."""
    if request.form.get('like') == 'like':
        like()
    elif request.form.get('unlike') == 'unlike':
        unlike()
    elif request.form.get('comment') == 'comment':
        add_comment()


def add_post_details(logname, postid):
    """Add Post Details."""
    connection = insta485.model.get_db()

    cur = connection.execute("SELECT * FROM posts WHERE postid = ?", (postid,))
    post = cur.fetchall()[0]
    owner = post['owner']
    img_url = "/uploads/" + post['filename']
    timestamp = arrow.get(post['created']).humanize(arrow.now())

    cur = connection.execute("SELECT filename FROM users WHERE username = ?",
                             (owner,))
    owner_img_url = "/uploads/" + cur.fetchall()[0]['filename']

    cur = connection.execute("SELECT COUNT(postid) FROM likes "
                             "WHERE postid = ?", (postid,))
    likes = cur.fetchall()[0]['COUNT(postid)']
    comments = get_comments(postid)

    cur = connection.execute("SELECT * FROM likes WHERE postid = ? "
                             "AND owner = ?", (postid, logname,))
    post_liked_by_logname = len(cur.fetchall()) == 1

    context = {"postid": postid,
               "owner": owner,
               "owner_img_url": owner_img_url,
               "img_url": img_url,
               "timestamp": timestamp,
               "likes": likes,
               "comments": comments,
               "post_liked_by_logname": post_liked_by_logname}

    return context


def validate_password(username, password):
    """Validate username and password against database records."""
    # Get (salt, password_db_string) and confirm that the user exists
    (salt, password_db_string) = get_salt(username)
    # Validate password
    hash_pass = hash_password(password, salt)
    if hash_pass != password_db_string:
        # abort(403, description="""incorrect password: {} hashed to {}\n
        # db_password: {}""".format(password, hash_pass, password_db_string))
        abort(403)


def hash_password(password, salt=uuid.uuid4().hex):
    """Hash password and return database-formatted string."""
    # Hash password and return '<algorithm>$<salt>$<hashed password>'
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string


def get_salt(username):
    """Return the salt associated with an existing username."""
    # Connect to database
    connection = insta485.model.get_db()
    # Get password_db_string
    password_db = connection.execute(
        "SELECT password FROM users WHERE username = ?", (username,)
    )
    # Confirm that the user exists
    password_db = password_db.fetchall()
    user_exists = len(password_db) > 0
    if not user_exists:
        abort(403)
    password_str = password_db[0]["password"]
    # Extract salt
    salt = password_str.split('$')[1]
    return (salt, password_str)
