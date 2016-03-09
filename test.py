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
    home_page = db.Column(db.String(500))
    developer = db.Column(db.String(500))
    developer_email = db.Column(db.String(500))
    developer_home_page = db.Column(db.String(200))
    problem = db.Column(db.String(500))
    algorithm = db.Column(db.String(200))
    language = db.Column(db.String(500))
    language_version = db.Column(db.String(500))
    release_date = db.Column(db.Date)
    release_version = db.Column(db.String(500))
    platforms = db.Column(db.String(500))
    lines_total = db.Column(db.String(500))
    lines_pure = db.Column(db.String(500))
    applications = db.Column(db.String(500))
    additional_information = db.Column(db.String(500))
    additional_attributes = db.Column(db.String(500))
    additional_attributes = db.Column(db.String(500))
    list_on_dist_algo_web_site = db.Column(db.String(500))
    submitter = db.Column(db.String(500))
    submitter_email = db.Column(db.String(500))
    home_page = db.Column(db.String(500))

    def __repr__(self):
        return '<project % r>' % self.title


class ProjectWrapper():
    def __init__(self, projects):
        print "init pw"
        self.projects = projects
        self.languages = {}
        for project in self.projects:
            if project.language in self.languages:
                if project.algorithm in self.languages[project.language]:
                    self.languages[project.language].append(project)
                else:
                    self.languages[project.language] = [project]
            else:
                self.languages[project.language] = {project.algorithm:[project]}

@app.route('/')
def index():
    response = make_response('web')
    response.set_cookie('test_cookie_key','test_cookie_value')
    projects = Project.query.all()
    pw = ProjectWrapper(projects)

    #print projects[0].title
    return render_template('index.html', projects=pw.languages)

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
    app.run(host= '0.0.0.0',port=5000, debug=True)
    #manager.run()
