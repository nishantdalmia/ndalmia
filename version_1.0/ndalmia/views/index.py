"""
Insta485 index (main) view.

URLs include:
/
"""
from flask import request, redirect, url_for, \
                  render_template
import insta485
import insta485.views.user
import insta485.views.followers
import insta485.views.following
import insta485.views.post
import insta485.views.explore
import insta485.views.login
import insta485.views.create
import insta485.views.delete
import insta485.views.edit
import insta485.views.uploads
from insta485.views.util import like_comment_post_request, \
                                add_post_details


@insta485.app.route('/', methods=['GET', 'POST'])
def show_index():
    """Display / route."""
    if 'username' in request.cookies:
        logname = request.cookies.get('username')

        if request.method == 'POST':
            like_comment_post_request()
        context = {'logname': logname,
                   'posts': get_post_details(logname)}
        return render_template('index.html', **context)

    return redirect(url_for('login'))


def get_post_details(logname):
    """Generate Post Details."""
    connection = insta485.model.get_db()

    cur = connection.execute("SELECT * FROM posts WHERE owner = ? UNION "
                             "SELECT * FROM posts WHERE owner IN "
                             "(SELECT username2 FROM following "
                             "WHERE username1 = ?)", (logname, logname,))
    posts = cur.fetchall()

    new_posts = list()
    for post in posts:
        new_posts.append(add_post_details(logname, post['postid']))

    return new_posts
