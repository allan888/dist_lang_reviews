from flask import Flask, render_template
from flask import make_response
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
manager = Manager(app)

@app.route('/')
def index():
    import json, request
    response = make_response('web')
    response.set_cookie('test_cookie_key','test_cookie_value')
    name = "world"
    return render_template('index.html', name=name)

@app.route('/user/<name>')
def user(name = 'world'):
    return render_template('user.html', name=name)

def run_before_first_request():
    pass

def run_teardown_request(args):
    pass

if __name__ == '__main__':
    app.before_first_request(run_before_first_request)
    app.teardown_request(run_teardown_request)
    #app.run(host= '0.0.0.0',port=5000, debug=True)
    manager.run()
