"""
ndalmia projects (main) view.

URLs include:
/projects/
"""
from flask import request, redirect, url_for, render_template
import ndalmia

@ndalmia.app.route('/projects/', methods=['GET', 'POST'])
def projects():
    """Display /projects/ route."""
    connection = ndalmia.model.get_db()
    cur = connection.execute("SELECT * FROM pposts")
    pposts = cur.fetchall()
    admin_logged_in = 'admin' in request.cookies

    context = {'admin_logged_in': admin_logged_in,
               'name': "Nishant Dalmia",
               'email': "ndalmia@umich.edu",
               'rmail': "ndalmia.recruit@gmail.com",
               'location': "Los Gatos, CA",
               'pposts': pposts}
    return render_template('projects.html', **context)
