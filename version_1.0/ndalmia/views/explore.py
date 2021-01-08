"""
Insta485 post view.

URLs include:
/explore/
"""
from flask import request, redirect, url_for, \
                  render_template
import insta485
from insta485.views.util import follow


@insta485.app.route('/explore/', methods=['GET', 'POST'])
def explore():
    """Display /p/<postid_url_slug>/ route."""
    if 'username' in request.cookies:
        logname = request.cookies.get('username')

        if request.method == 'POST':
            if request.form.get('follow') == 'follow':
                follow(logname, request.form['username'])

        return get_explore(logname)

    return redirect(url_for('login'))


def get_explore(logname):
    """Explore."""
    # Connect to database
    connection = insta485.model.get_db()

    cur = connection.execute("SELECT * FROM users WHERE username != ? "
                             "AND username NOT IN (SELECT username2 "
                             "FROM following WHERE username1 = ?)",
                             (logname, logname,))
    not_following = cur.fetchall()
    not_following_details = get_explore_details(not_following)

    context = {"logname": logname,
               "not_following": not_following_details}
    return render_template('explore.html', **context)


def get_explore_details(not_following):
    """Generate explore details."""
    not_following_details = list()
    for user in not_following:
        user_img_url = "/uploads/" + user['filename']
        user_details = {"username": user['username'],
                        "user_img_url": user_img_url}
        not_following_details.append(user_details)

    return not_following_details
