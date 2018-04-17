import random
import string

from flask import Flask, request, session, abort, render_template, jsonify

app = Flask(__name__)
app.secret_key = "<generate your own secret key>"


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/post/', methods=['POST'])
def test_post():
    if request.method == "POST":
        print(request.get_json()['test'])
        return jsonify({"success": "yay"})


@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.headers.get("X-Csrftoken", None):
            abort(403)


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = some_random_string(64)
    return session['_csrf_token']


def some_random_string(size):
    return ''.join(random.SystemRandom().choice(
        string.ascii_uppercase +
        string.ascii_lowercase +
        string.digits
    ) for _ in range(size))


app.jinja_env.globals['csrf_token'] = generate_csrf_token

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5005)
