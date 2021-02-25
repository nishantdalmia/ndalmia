"""
ndalmia index (main) view.

URLs include:
/
"""
from flask import request, redirect, url_for, render_template
import ndalmia
import ndalmia.views.login
import ndalmia.views.work
import ndalmia.views.projects
import ndalmia.views.epost
import ndalmia.views.wpost
import ndalmia.views.ppost
import ndalmia.views.uploads

@ndalmia.app.route('/', methods=['GET', 'POST'])
def show_index():
    """Display / route."""
    connection = ndalmia.model.get_db()
    cur = connection.execute("SELECT * FROM eposts")
    eposts = cur.fetchall()
    for epost in eposts:
        epost['image_url'] = "/uploads/" + epost['filename']
    aboutme = 'I am currently a senior pursuing a major in ' + 'Computer Science and a minor in Physics at the University of ' + 'Michigan at Ann Arbor. I am ' + 'passionate about my work and what I do. ' + 'I consider myself a person who can solve problems ' + 'be it in my academic, work or personal life. I am ' + 'eager to work in and with the Technology community to ' + 'learn more about it and add value to it. '
    admin_logged_in = 'admin' in request.cookies

    context = {'admin_logged_in': admin_logged_in,
               'name': "Nishant Dalmia",
               'email': "ndalmia@umich.edu",
               'location': "Ann Arbor, MI",
               'aboutme': aboutme,
               'eposts': eposts}
    return render_template('index.html', **context)
