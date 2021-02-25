"""
ndalmia project post (main) view.

URLs include:
/p/
/p/delete/
"""
from flask import request, redirect, url_for, render_template, make_response
import ndalmia

@ndalmia.app.route('/p/', methods=['GET', 'POST'])
def ppost():
    """Display /p/ route."""
    if request.method == 'POST' :
        connection = ndalmia.model.get_db()
        connection.execute(
        "INSERT INTO pposts(title, description, location, link) "
        "VALUES(?, ?, ?, ?)",
        (request.form['title'], request.form['description'], request.form['location'],
         request.form['link'],))

        return make_response(redirect(url_for('projects')))

    context = {'name': "Nishant Dalmia",
               'email': "ndalmia@umich.edu",
               'location': "Ann Arbor, MI"}
    return render_template('ppost.html', **context)


@ndalmia.app.route('/p/delete/', methods=['GET', 'POST'])
def delete_ppost():
    """Delete Projects Post."""
    ppostid = request.form['delete']
    connection = ndalmia.model.get_db()
    connection.execute("DELETE FROM pposts WHERE ppostid = ?", (ppostid,))

    return make_response(redirect(url_for('projects')))
