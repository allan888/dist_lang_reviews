import csv
import json
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
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

with open('dataSource.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, skipinitialspace = True)
    for row in reader:
        pj = Project(title=row[0].strip(),home_page=row[1].strip(),developer=row[2].strip(),
        developer_email=row[3].strip(),developer_home_page=row[4].strip(),
        problem=row[5].strip(),algorithm=row[6].strip(),language=row[7].strip(),
        language_version=row[8].strip(),release_date=row[9].strip(),lines_total=row[10].strip(),
        lines_pure=row[11].strip(),additional_information=row[12].strip(),
        additional_attributes=row[13].strip(),release_version=row[14].strip(),
        list_on_dist_algo_web_site=row[15].strip(),applications=row[16].strip())
        db.session.add(pj)
    db.session.commit()
