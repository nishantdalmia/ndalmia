"""
Insta485 user followers page view.

URLs include:
/u/<user_url_slug>/followers/
"""
from flask import request, redirect, url_for, render_template
import insta485
from insta485.views.util import validate, follow_post_request


@insta485.app.route('/u/<path:username>/followers/', methods=['GET', 'POST'])
def show_user_followers(username):
    """Display /u/<user_url_slug>/followers/ route."""
    if 'username' in request.cookies:
        logname = request.cookies.get('username')

        validate(username)
        follow_post_request(logname)
        return get_user_followers(logname, username)

    return redirect(url_for('login'))


def get_user_followers(logname, username):
    """Generate user followers."""
    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    cur = connection.execute("SELECT username1 FROM following "
                             "WHERE username2 = ?", (username,))
    followers = cur.fetchall()
    followers_details = get_followers(logname, followers)

    context = {"logname": logname,
               "username": username,
               "followers": followers_details}
    return render_template('followers.html', **context)


def get_followers(logname, followers):
    """Generate follower details."""
    # Connect to database
    connection = insta485.model.get_db()

    new_followers = list()
    for follower in followers:
        cur = connection.execute("SELECT filename FROM users "
                                 "WHERE username = ?",
                                 (follower['username1'],))
        user_img_url = "/uploads/" + cur.fetchall()[0]['filename']

        cur = connection.execute("SELECT * FROM following WHERE username1 = ? "
                                 "AND username2 = ?",
                                 (logname, follower['username1'],))
        logname_follows_username = len(cur.fetchall()) == 1

        new_follower = {"username": follower['username1'],
                        "user_img_url": user_img_url,
                        "logname_follows_username": logname_follows_username}
        new_followers.append(new_follower)

    return new_followers
