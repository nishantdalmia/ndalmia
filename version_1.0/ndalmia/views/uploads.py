"""
ndalmia uploads view.

URLs include:
/uploads/<filename>/
"""
from flask import request, send_from_directory, abort
import ndalmia


@ndalmia.app.route('/uploads/<path:filename>')
def show_upload(filename):
    """Display static uploaded file."""
    # Abort if user is not logged in
    return send_from_directory(str(ndalmia.app.config["UPLOAD_FOLDER"]),
                                   filename)

    return abort(403)
