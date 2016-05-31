#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from flask import make_response
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
import random
import sys
import inspect
from sqlalchemy import desc


app = Flask(__name__)
Bootstrap(app)
manager = Manager(app)


db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://webadmin:webadmin123.@s2.zhujieao.com/dist'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    email = db.Column(db.String(200))
    name = db.Column(db.String(500))
    date = db.Column(db.DateTime)
    point = db.Column(db.Float)
    content = db.Column(db.Text)

    def serialize(self):
        return {
            'id': self.id,
            'pid': self.pid,
            'email': self.email,
            'name': self.name,
            'date': str(self.date),
            'point': self.point,
            'content': self.content
        }

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
    list_on_dist_algo_web_site = db.Column(db.String(500))
    submitter = db.Column(db.String(500))
    submitter_email = db.Column(db.String(500))
    score = db.Column(db.Float)

    def __repr__(self):
        return '<project % r>' % self.title

    def __init__(self, title, home_page, developer, developer_email, problem, algorithm, language, \
    language_version, release_date, release_version, platforms, lines_total, lines_pure, applications, \
    additional_information, additional_attributes,list_on_dist_algo_web_site, submitter, submitter_email):
        self.title = title
        self.home_page = home_page
        self.developer = developer
        self.developer_email = developer_email
        self.problem = problem
        self.algorithm = algorithm
        self.language = language
        self.language_version = language_version
        self.release_date = release_date
        self.release_version = release_version
        self.platforms = platforms
        self.lines_total = lines_total
        self.lines_pure = lines_pure
        self.applications = applications
        self.additional_information = additional_information
        self.additional_attributes = additional_attributes
        self.list_on_dist_algo_web_site = list_on_dist_algo_web_site
        self.submitter = submitter
        self.submitter_email = submitter_email
        self.score = 0.0

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'home_page': self.home_page,
            'developer': self.developer,
            'developer_email': self.developer_email,
            'developer_home_page': self.developer_home_page,
            'problem': self.problem,
            'algorithm': self.algorithm,
            'language': self.language,
            'language_version': self.language_version,
            'release_date': str(self.release_date),
            'release_version': self.release_version,
            'lines_total': self.lines_total,
            'lines_pure': self.lines_pure,
            'platforms': self.platforms,
            'applications': self.applications,
            'additional_information': self.additional_information,
            'additional_attributes': self.additional_attributes,
            'list_on_dist_algo_web_site': self.list_on_dist_algo_web_site,
            'submitter': self.submitter,
            'submitter_email': self.submitter_email,
            'score': self.score
        }

class ProjectWrapper():
    def __init__(self, projects, type='language'):
        self.projects = projects
        self.languages = {}
        for project in self.projects:
            if type == 'language':
                items = project.language.split(',')
            else:
                items = project.problem.split(',')
            items = map(lambda x:x.strip(), items)
            for item in items:
                if item != '':
                    if item in self.languages:
                        self.languages[item].append(project)
                    else:
                        self.languages[item] = [project]
        keys = list(self.languages.keys())
        keys.sort()
        new_list = []
        for key in keys:
            new_list.append((key, sorted(self.languages[key], key=lambda p: p.title)))
        self.languages = new_list

db_all_projects = Project.query.order_by(desc(Project.score)).all()

def strip(x):
    return x.strip()
def getTitle(x):
    return x.title

def sortByTitle(grouped):
    new_list = []
    keys = list(grouped.keys())
    keys.sort()
    for key in keys:
        new_list.append((key, sorted(grouped[key], key = getTitle)))
    return new_list

def render(page, p=None):
    if p is not None:
        return render_template(page, projects=p)
    else:
        return render_template(page)
