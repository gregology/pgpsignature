import sqlite3, re
from flask import Flask, Response, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

A_UPPERCASE = ord('A')
ALPHABET_SIZE = 26
PGP_SIGNATURE_REGEX = '^-----BEGIN PGP SIGNED MESSAGE-----(.*\n)*-----BEGIN PGP SIGNATURE-----(.*\n)*-----END PGP SIGNATURE-----$'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_signature(signature_id):
    conn = get_db_connection()
    signature = conn.execute('SELECT * FROM signatures WHERE id = ?',
                        (signature_id,)).fetchone()
    conn.close()
    if signature is None:
        abort(404)
    return signature


def _decompose(number):
    while number:
        number, remainder = divmod(number - 1, ALPHABET_SIZE)
        yield remainder


def base_10_to_alphabet(number):
    return ''.join(
            chr(A_UPPERCASE + part)
            for part in _decompose(number)
    )[::-1]


def base_alphabet_to_10(letters):
    """Convert an alphabet number to its decimal representation"""

    return sum(
            (ord(letter) - A_UPPERCASE + 1) * ALPHABET_SIZE**i
            for i, letter in enumerate(reversed(letters.upper()))
    )


def clean_content(content):
    return content.strip()

app = Flask(__name__)


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        content = clean_content(request.form['content'])
        is_pgp_signature = bool(re.search(PGP_SIGNATURE_REGEX, content))

        if not content:
            flash('signature content is required!')
        elif not is_pgp_signature:
            flash('this is not a pgp signature')
        else:
            conn = get_db_connection()
            cursor = conn.execute('INSERT INTO signatures (content) VALUES (?)',
                         (content,))
            conn.commit()
            signature_id = cursor.lastrowid
            signature_key = base_10_to_alphabet(signature_id)
            conn.close()
            return redirect(url_for('signature', signature_key=signature_key))

    return render_template('index.html')


@app.route('/<string:signature_key>.asc')
def get_file(signature_key):
    signature_id = base_alphabet_to_10(signature_key)
    signature = get_signature(signature_id)
    results = signature['content']
    generator = (cell for row in results
                    for cell in row)

    return Response(generator,
                       mimetype='text/plain',
                       headers={'Content-Disposition':
                                    f'attachment;filename={signature_key}.asc'})


@app.route('/<string:signature_key>')
def signature(signature_key):
    signature_id = base_alphabet_to_10(signature_key)
    signature = get_signature(signature_id)
    return render_template('signature.html', signature=signature, signature_key=signature_key)
