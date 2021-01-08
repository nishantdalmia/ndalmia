"""
Insta485 uploads view.

URLs include:
/uploads/<filename>/
"""
from flask import request, send_from_directory, abort
import insta485


@insta485.app.route('/uploads/<path:filename>')
def show_upload(filename):
    """Display static uploaded file."""
    # Abort if user is not logged in
    if 'username' in request.cookies:
        return send_from_directory(str(insta485.app.config["UPLOAD_FOLDER"]),
                                   filename)

    return abort(403)
