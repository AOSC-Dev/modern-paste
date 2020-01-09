import os
import json

import flask
import subprocess

from api.decorators import render_view
from modern_paste import app
from uri.misc import *


@app.route(APIDocumentationInterfaceURI.path, methods=['GET'])
@render_view
def api_documentation_interface():
    """
    Documentation for all publicly exposed API endpoints.
    """
    data_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '../templates/misc/api_documentation.json'
    )
    with open(data_path, 'rt') as f:
        api_documentation_data = json.load(f)
    return 'misc/api_documentation.html', {
        'api_endpoints': api_documentation_data['api_endpoints'],
        'generic_error_responses': api_documentation_data['generic_error_responses'],
    }


@app.route(VersionURI.path, methods=['GET', 'POST'])
def version():
    """
    Show the currently-deployed version of the app.
    """
    branch_name = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).replace(b'\n', b'')
    commit_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD']).replace(b'\n', b'')
    commit_date = subprocess.check_output(['git', 'log', '-1', '--format=%cd']).replace(b'\n', b'')
    remote_url = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url']).replace(b'\n', b'')

    version_string = '{branch}\n{sha}\n{date}\n{url}'.format(
        branch=branch_name.decode('utf-8'),
        sha=commit_sha.decode('utf-8'),
        date=commit_date.decode('utf-8'),
        url=remote_url.decode('utf-8'),
    )

    return flask.Response(version_string, mimetype='text/plain')
