import json
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from flask import make_response
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap






app = Flask(__name__)
Bootstrap(app)
manager = Manager(app)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://webadmin:webadmin123.@s2.zhujieao.com/dist'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    def __repr__(self):
        return '<project % r>' % self.title

@app.route('/')
def index():
    response = make_response('web')
    response.set_cookie('test_cookie_key','test_cookie_value')
    projects = Project.query.all()
    print Project
    print projects
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
