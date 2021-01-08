"""
Insta485 user following page view.

URLs include:
/u/<user_url_slug>/following/
"""
from flask import request, redirect, url_for, render_template
import insta485
from insta485.views.util import validate, follow_post_request


@insta485.app.route('/u/<path:username>/following/', methods=['GET', 'POST'])
def show_user_following(username):
    """Display /u/<user_url_slug>/following/ route."""
    if 'username' in request.cookies:
        logname = request.cookies.get('username')

        validate(username)
        follow_post_request(logname)
        return get_user_following(logname, username)

    return redirect(url_for('login'))


def get_user_following(logname, username):
    """Generate user following."""
    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    cur = connection.execute("SELECT username2 FROM following "
                             "WHERE username1 = ?", (username,))
    following = cur.fetchall()
    following_details = get_following(logname, following)

    context = {"logname": logname,
               "username": username,
               "following": following_details}
    return render_template('following.html', **context)


def get_following(logname, following):
    """Generate following details."""
    # Connect to database
    connection = insta485.model.get_db()

    new_following = list()
    for follower in following:
        cur = connection.execute("SELECT filename FROM users "
                                 "WHERE username = ?",
                                 (follower['username2'],))
        user_img_url = "/uploads/" + cur.fetchall()[0]['filename']

        cur = connection.execute("SELECT * FROM following "
                                 "WHERE username1 = ? AND username2 = ?",
                                 (logname, follower['username2'],))
        logname_follows_username = len(cur.fetchall()) == 1

        new_follower = {"username": follower['username2'],
                        "user_img_url": user_img_url,
                        "logname_follows_username": logname_follows_username}
        new_following.append(new_follower)

    return new_following
