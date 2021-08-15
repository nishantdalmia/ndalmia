"""
ndalmia education post (main) view.

URLs include:
/e/
/e/delete/
"""
from flask import request, redirect, url_for, render_template, make_response
import pathlib
import uuid
import ndalmia

@ndalmia.app.route('/e/', methods=['GET', 'POST'])
def epost():
    """Display /e/ route."""
    if request.method == 'POST' :
        fileobj = request.files['file']
        filename = fileobj.filename
        uuid_basename = "{stem}{suffix}".format(
            stem=uuid.uuid4().hex,
            suffix=pathlib.Path(filename).suffix)
        fileobj.save(ndalmia.app.config["UPLOAD_FOLDER"]/uuid_basename)

        connection = ndalmia.model.get_db()
        connection.execute(
        "INSERT INTO eposts(filename, institution, major, start_time, end_time) "
        "VALUES(?, ?, ?, ?, ?)",
        (uuid_basename, request.form['institution'], request.form['major'],
         request.form['start_time'], request.form['end_time'],))

        return make_response(redirect(url_for('show_index')))

    context = {'name': "Nishant Dalmia",
               'email': "ndalmia@umich.edu",
               'rmail': "ndalmia.recruit@gmail.com",
               'location': "Los Gatos, CA"}
    return render_template('epost.html', **context)



@ndalmia.app.route('/e/delete/', methods=['GET', 'POST'])
def delete_epost():
    """Delete Education Post."""
    epostid = request.form['delete']
    connection = ndalmia.model.get_db()
    cur = connection.execute("SELECT filename FROM eposts WHERE epostid = ?", (epostid, ))

    epost = cur.fetchall()[0]
    filename = epost['filename']
    path = ndalmia.app.config["UPLOAD_FOLDER"]/filename
    path.unlink()
    connection.execute("DELETE FROM eposts WHERE epostid = ?", (epostid,))

    return make_response(redirect(url_for('show_index')))
