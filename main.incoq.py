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
from incoq.runtime import *
from orm import *


def group(projects):
    # Cost: O(((? * projects) + (items * projects)))
    #       O(((? * projects) + (items * projects)))
    ProjectsGroupByLanguage = Map()
    ProjectsGroupByProblem = Map()
    for p in projects:
        lan_col = p.language.split(',')
        pro_col = p.problem.split(',')
        lans = map(strip, lan_col)
        problems = map(strip, pro_col)
        for lan in lans:
            if (lan != ''):
                if (lan in ProjectsGroupByLanguage):
                    ProjectsGroupByLanguage[lan].add(p)
                else:
                    ProjectsGroupByLanguage[lan] = Set()
                    ProjectsGroupByLanguage[lan].add(p)
        for problem in problems:
            if (problem != ''):
                if (problem in ProjectsGroupByProblem):
                    ProjectsGroupByProblem[problem].add(p)
                else:
                    ProjectsGroupByProblem[problem] = Set()
                    ProjectsGroupByProblem[problem].add(p)
    return sortByTitle(ProjectsGroupByLanguage), sortByTitle(ProjectsGroupByProblem)

p_by_language, p_by_problem = group(db_all_projects)




# @app.route('/')
def index():
    query = {}
    query['groupBy'] = request.args.get('groupBy','')
    response = make_response('web')
    if query['groupBy'] == 'problem':
        return render('index_groupby_problem.html', p_by_problem)
    else:
        return render('index.html', p_by_language)
app.route('/')(index)

# @app.route('/index', methods=['POST', 'GET'])
def index2():
    query = {}
    query['groupBy'] = request.args.get('groupBy','')
    response = make_response('web')
    pw = None
    if query['groupBy'] == 'problem':
        return render_template('index_groupby_problem.html', projects=p_by_problem)
    else:
        return render_template('index.html', projects=p_by_language)
app.route('/index', methods=['POST', 'GET'])(index2)



@app.route('/test')
def test():
    response = make_response('web')
    projects = Project.query.order_by(desc(Project.score)).all()

    projects_python = Set()
    projects_github = Set()
    for p in projects:
        if ('python' in map(strip, p.language.lower().split(','))):
            projects_python.add(p)
        if ('github' in p.home_page):
            projects_github.add(p)
    print({p1.developer for p1 in projects_python if (p1 in projects_github)})
    return render('index.html', p_by_language)
app.route('/test')(test)

# @app.route('/user/<name>')
# def user(name = 'world'):
#     return render_template('user.html', name=name)
# app.route('/user/<name>')(user)

# @app.route('/advanced')
def advanced():
    return render_template('advanced.html')
app.route('/advanced')(advanced)

# @app.route('/submit',methods=['POST', 'GET'])
def submit():
    title = request.args.get('title','')
    if title != '':
        home_page = request.args.get('home_page','')
        developer = request.args.get('developer','')
        developer_email = request.args.get('developer_email','')
        developer_home_page = request.args.get('developer_home_page','')
        problem = request.args.get('problem','')
        algorithm = request.args.get('algorithm','')
        release_date = request.args.get('release_date','')
        release_version = request.args.get('release_version','')
        platforms = request.args.get('platforms','')
        language = request.args.get('language','')
        language_version = request.args.get('language_version','')
        lines_total = request.args.get('lines_total','')
        lines_pure = request.args.get('lines_pure','')
        applications = request.args.get('applications','')
        additional_information = request.args.get('additional_information','')
        additional_attributes = request.args.get('additional_attributes','')
        list_on_distalgo_web_site = request.args.get('list_on_distalgo_web_site','')
        submitter = request.args.get('submitter','')
        submitter_email = request.args.get('submitter_email','')
        project = Project(title, home_page, developer, developer_email, problem, algorithm, language, \
        language_version, release_date, release_version, platforms, lines_total, lines_pure, applications, \
        additional_information, additional_attributes,list_on_distalgo_web_site, submitter, submitter_email)
        db.session.add(project)
        db.session.commit()
    return render_template('submit.html')
app.route('/submit',methods=['POST', 'GET'])(submit)

# @app.route('/API/search', methods=['POST', 'GET'])
def searchapi():
    query = {}
    query['title'] = request.args.get('title','')
    query['developer_email'] = request.args.get('developer_email','')
    query['additional_information'] = request.args.get('additional_information','')
    query['home_page'] = request.args.get('home_page','')
    query['language'] = request.args.get('language','')
    query['platforms'] = request.args.get('platform','')
    query['algorithm'] = request.args.get('algorithm','')
    query['problem'] = request.args.get('problem','')
    no_parameter = True
    lang = query['language']
    for q in query:
        if query[q] != '':
            no_parameter = False
        query[q] = '%{0}%'.format(query[q])
    if no_parameter:
        return 'error'
    # tilte = '%{0}%'.format(tilte)
    # developer_email = '%{0}%'.format(developer_email)
    # additional_information = '%{0}%'.format(additional_information)
    # home_page = '%{0}%'.format(home_page)
    # language = '%{0}%'.format(language)
    # platforms = '%{0}%'.format(platforms)
    # algorithm = '%{0}%'.format(algorithm)
    # problem = '%{0}%'.format(problem)

    qs = [ getattr(getattr(Project, k),'ilike')(query[k]) for k in query if query[k] != '%%' and query[k] != '']
    projects = Project.query.filter(  *qs ).order_by(desc(Project.score)).all()
        # Project.title.ilike(query['title']),\
        # Project.developer_email.ilike(query['developer_email']),\
        # Project.additional_information.ilike(query['additional_information']),\
        # Project.home_page.ilike(query['home_page']),\
        # Project.language.ilike(query['language']),\
        # Project.platforms.ilike(query['platforms']),\
        # Project.algorithm.ilike(query['algorithm']),\
        # Project.problem.ilike(query['problem'])
    # )

    return json.dumps([e.serialize() for e in projects])
app.route('/API/search', methods=['POST', 'GET'])(searchapi)


# @app.route('/search', methods=['POST', 'GET'])
def search():
    query = {}
    query['title'] = request.args.get('title','')
    query['developer_email'] = request.args.get('developer_email','')
    query['additional_information'] = request.args.get('additional_information','')
    query['home_page'] = request.args.get('home_page','')
    query['language'] = request.args.get('language','')
    query['platforms'] = request.args.get('platform','')
    query['algorithm'] = request.args.get('algorithm','')
    query['problem'] = request.args.get('problem','')
    no_parameter = True
    lang = query['language']
    for q in query:
        if query[q] != '':
            no_parameter = False
        query[q] = '%{0}%'.format(query[q])
    if no_parameter:
        return 'error'
    # tilte = '%{0}%'.format(tilte)
    # developer_email = '%{0}%'.format(developer_email)
    # additional_information = '%{0}%'.format(additional_information)
    # home_page = '%{0}%'.format(home_page)
    # language = '%{0}%'.format(language)
    # platforms = '%{0}%'.format(platforms)
    # algorithm = '%{0}%'.format(algorithm)
    # problem = '%{0}%'.format(problem)

    qs = [ getattr(getattr(Project, k),'ilike')(query[k]) for k in query if query[k] != '%%' and query[k] != '']
    projects = Project.query.filter(  *qs ).order_by(desc(Project.score)).all()
        # Project.title.ilike(query['title']),\
        # Project.developer_email.ilike(query['developer_email']),\
        # Project.additional_information.ilike(query['additional_information']),\
        # Project.home_page.ilike(query['home_page']),\
        # Project.language.ilike(query['language']),\
        # Project.platforms.ilike(query['platforms']),\
        # Project.algorithm.ilike(query['algorithm']),\
        # Project.problem.ilike(query['problem'])
    # )
    pw = ProjectWrapper(projects)
    search_by_lang = False
    for k in query:
        if query[k] != '%%' and query[k] != '' and k == 'language':
            search_by_lang = True

    if search_by_lang:
        for l in pw.languages:
            if str.lower(str(lang)) == str.lower(str(l)):
                lang = l
        return render_template('search.html', projects={lang: pw.languages[lang]})
    else:
        return render_template('search.html', projects=pw.languages)
app.route('/search', methods=['POST', 'GET'])(search)

# @app.route('/API/comments/<pid>')
def getComments(pid):
    project = int(pid)
    comments = Comment.query.filter_by(pid=project).all()
    return json.dumps([e.serialize() for e in comments])
app.route('/API/comments/<pid>')(getComments)

# @app.route('/API/allProjects')
def allProjects():
    projects = Project.query.order_by(desc(Project.score)).all()
    return json.dumps([e.serialize() for e in projects])
app.route('/API/allProjects')(allProjects)

# @app.route('/API/project/<pid>')
def getProjects(pid):
    pid = int(pid)
    project = Project.query.filter_by(id=pid).first()
    return json.dumps(project.serialize())
app.route('/API/project/<pid>')(getProjects)

# @app.route('/submitComment/<pid>', methods=['POST', 'GET'])
def putComments(pid):
    project = int(pid)
    email = request.form.get('email','err')
    name = request.form.get('name','err')
    content = request.form.get('content','err')
    point = request.form.get('point','err')
    if email == 'err' or content == 'err' or point == 'err' or name == 'err':
        return 'error'
    comment = Comment(pid=pid, email=email, name=name, content=content, point=point)
    db.session.add(comment)
    db.session.commit()
    return render_template('goBack.html')
app.route('/submitComment/<pid>', methods=['POST', 'GET'])(putComments)

# @app.route('/sqlSearch', methods=['POST', 'GET'])
def sqlSearch():
    sql = request.form.get('sql','')
    res = []
    if sql != '':
        if sql != '' and 'drop' not in sql and 'delete' not in sql and 'update' not in sql:
            try:
                results = db.engine.execute(sql)
            except:
                results = None
                res.append('illegal sql query')
            if results is not None:
                for row in results:
                    res.append(list(row))
        else:
            res.append('do not update/delete/drop table')
    res = json.dumps(res)
    if sql == '':
        sql = "select `title` from `projects`"
    return render_template('sql.html', sql=sql, json=res)
app.route('/sqlSearch', methods=['POST', 'GET'])(sqlSearch)

def run_before_first_request():
    pass

def run_teardown_request(args):
    pass



if __name__ == '__main__':
    app.before_first_request(run_before_first_request)
    app.teardown_request(run_teardown_request)
    app.run(host= '0.0.0.0',port=5000, debug=True)
    #manager.run()
