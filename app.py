from flask import Flask, request, render_template, jsonify, redirect
from git_utils import get_git_data,authenticate_user
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'this is the secret key'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return {'message': "token is missing"}
        try:
            data = jwt.decode(token,app.secret_key)
            return f(data,*args, **kwargs)
        except:
            return {'message': "token is missing"}
    return decorated

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        # getting user info from entry
        submit_info = request.form

        if '' not in submit_info.values():
            if authenticate_user(submit_info):
                token = jwt.encode({"user": submit_info['user'],
                                    "password": submit_info['password'],
                                    'repository': submit_info['repository'],
                                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                                   app.secret_key)

                return redirect("/repo?token="+token.decode('UTF-8'))
        else:
            return {"Error": 'There was a problem with your username or password'}
    # rendering home page
    return render_template('home_page.html')

@app.route("/repo")
@token_required
def repo(data):
    return get_git_data(data)


if __name__ == "__main__":
    app.run()
