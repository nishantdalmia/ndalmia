"""
ndalmia work post (main) view.

URLs include:
/w/
/w/delete/
"""
from flask import request, redirect, url_for, render_template, make_response
import pathlib
import uuid
import ndalmia

@ndalmia.app.route('/w/', methods=['GET', 'POST'])
def wpost():
    """Display /w/ route."""
    if request.method == 'POST' :
        fileobj = request.files['file']
        filename = fileobj.filename
        uuid_basename = "{stem}{suffix}".format(
            stem=uuid.uuid4().hex,
            suffix=pathlib.Path(filename).suffix)
        fileobj.save(ndalmia.app.config["UPLOAD_FOLDER"]/uuid_basename)

        connection = ndalmia.model.get_db()
        connection.execute(
        "INSERT INTO wposts(filename, company, title, description, location, start_time, end_time) "
        "VALUES(?, ?, ?, ?, ?, ?, ?)",
        (uuid_basename, request.form['company'], request.form['title'],
         request.form['description'], request.form['location'], request.form['start_time'],
         request.form['end_time'],))

        return make_response(redirect(url_for('work')))

    context = {'name': "Nishant Dalmia",
               'email': "ndalmia@umich.edu",
               'location': "Ann Arbor, MI"}
    return render_template('wpost.html', **context)

@ndalmia.app.route('/w/delete/', methods=['GET', 'POST'])
def delete_wpost():
    """Delete Work Post."""
    wpostid = request.form['delete']
    connection = ndalmia.model.get_db()
    cur = connection.execute("SELECT filename FROM wposts WHERE wpostid = ?", (wpostid, ))

    wpost = cur.fetchall()[0]
    filename = wpost['filename']
    path = ndalmia.app.config["UPLOAD_FOLDER"]/filename
    path.unlink()
    connection.execute("DELETE FROM wposts WHERE wpostid = ?", (wpostid,))

    return make_response(redirect(url_for('work')))
