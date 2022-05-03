import re, os
from flask import Flask, Response, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Signature


def base_alphabet_to_10(letters):
    return sum(
            (ord(letter) - Signature.A_UPPERCASE + 1) * Signature.ALPHABET_SIZE**i
            for i, letter in enumerate(reversed(letters.upper()))
    )


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        content = request.form['content']

        try:
            signature = Signature(content=content)
        except AssertionError as assertionError:
            flash(assertionError)
        else:
            db.session.add(signature)
            db.session.commit()
            return redirect(url_for('signature', signature_key=signature.key()))

    return render_template('index.html')


@app.route('/<string:signature_key>.asc')
def get_file(signature_key):
    signature_id = base_alphabet_to_10(signature_key)
    signature = Signature.query.get(signature_id)

    if signature is None:
        abort(404)
    else:
        generator = (cell for row in signature.content for cell in row)

        return Response(
            generator,
            mimetype='text/plain',
            headers={
                'Content-Disposition': f'attachment;filename={signature_key}.asc'
                }
            )


@app.route('/<string:signature_key>')
def signature(signature_key):
    signature_id = base_alphabet_to_10(signature_key)
    signature = Signature.query.get(signature_id)
    if signature is None:
        abort(404)
    else:
        return render_template(
            'signature.html',
            signature=signature,
            signature_key=signature_key
        )
