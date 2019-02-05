import base64
import io
from flask import make_response, send_file


def make_pixel_response():

    data_64 = 'R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'.encode(
        'ascii')
    data = base64.decodebytes(data_64)
    return send_file(io.BytesIO(data), mimetype='image/gif')
