"""
ndalmia work (main) view.

URLs include:
/work/
"""
from flask import request, redirect, url_for, render_template
import ndalmia

@ndalmia.app.route('/work/', methods=['GET', 'POST'])
def work():
    """Display /work/ route."""
    connection = ndalmia.model.get_db()
    cur = connection.execute("SELECT * FROM wposts")
    wposts = cur.fetchall()
    for wpost in wposts:
        wpost['image_url'] = "/uploads/" + wpost['filename']
    admin_logged_in = 'admin' in request.cookies

    context = {'admin_logged_in': admin_logged_in,
               'name': "Nishant Dalmia",
               'email': "ndalmia@umich.edu",
               'rmail': "ndalmia.recruit@gmail.com",
               'location': "Los Gatos, CA",
               'wposts': wposts}
    return render_template('work.html', **context)
