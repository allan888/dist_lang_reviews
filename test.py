from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hel3lo1 2Worl32d1123232323231!</h1>',400

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, % s!</h1>' % name

def run_before_first_request():
    pass

def run_teardown_request(args):
    pass

if __name__ == '__main__':
    app.before_first_request(run_before_first_request)
    app.teardown_request(run_teardown_request)
    app.run(host= '0.0.0.0',port=80, debug=True)
