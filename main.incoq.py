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
def index1():
    query = {}
    query['groupBy'] = request.args.get('groupBy','')
    response = make_response('web')
    if query['groupBy'] == 'problem':
        return render('index_groupby_problem.html', p_by_problem)
    else:
        return render('index.html', p_by_language)
app.route('/')(index1)

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











# _U_Q : {({Bottom}, {Bottom})}
_U_Q = Set()
# R_Q : {({Bottom}, {Bottom}, Top)}
R_Q = CSet()
# _U_Q_bu : {{Bottom}: {{Bottom}}}
_U_Q_bu = Map()
# _U_Q_ub : {{Bottom}: {{Bottom}}}
_U_Q_ub = Map()
# _M_ub : {Top: {Top}}
_M_ub = Map()
# R_Q_bbu : {({Bottom}, {Bottom}): {Top}}
R_Q_bbu = Map()
def _maint__U_Q_bu_for__U_Q_add(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v9_key = _elem_v1
    _v9_value = _elem_v2
    if (_v9_key not in _U_Q_bu):
        _v10 = Set()
        _U_Q_bu[_v9_key] = _v10
    _U_Q_bu[_v9_key].add(_v9_value)

def _maint__U_Q_ub_for__U_Q_add(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v12_key = _elem_v2
    _v12_value = _elem_v1
    if (_v12_key not in _U_Q_ub):
        _v13 = Set()
        _U_Q_ub[_v12_key] = _v13
    _U_Q_ub[_v12_key].add(_v12_value)

def _maint__M_ub_for__M_add(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v15_key = _elem_v2
    _v15_value = _elem_v1
    if (_v15_key not in _M_ub):
        _v16 = Set()
        _M_ub[_v15_key] = _v16
    _M_ub[_v15_key].add(_v15_value)

def _maint_R_Q_bbu_for_R_Q_add(_elem):
    (_elem_v1, _elem_v2, _elem_v3) = _elem
    _v18_key = (_elem_v1, _elem_v2)
    _v18_value = _elem_v3
    if (_v18_key not in R_Q_bbu):
        _v19 = Set()
        R_Q_bbu[_v18_key] = _v19
    R_Q_bbu[_v18_key].add(_v18_value)

def _maint_R_Q_bbu_for_R_Q_remove(_elem):
    (_elem_v1, _elem_v2, _elem_v3) = _elem
    _v20_key = (_elem_v1, _elem_v2)
    _v20_value = _elem_v3
    R_Q_bbu[_v20_key].remove(_v20_value)
    if (len(R_Q_bbu[_v20_key]) == 0):
        del R_Q_bbu[_v20_key]

def _maint_R_Q_for__U_Q_add(_elem):
    # Cost: O(_v3_projects_python)
    #       O(_v3_projects_python)
    (_v3_projects_python, _v3_projects_github) = _elem
    if isset(_v3_projects_python):
        for _v3_p1 in _v3_projects_python:
            if isset(_v3_projects_github):
                if (_v3_p1 in _v3_projects_github):
                    if hasfield(_v3_p1, 'developer'):
                        _v3_p1_developer = _v3_p1.developer
                        _v3_result = (_v3_projects_python, _v3_projects_github, _v3_p1_developer)
                        if (_v3_result not in R_Q):
                            R_Q.add(_v3_result)
                            _maint_R_Q_bbu_for_R_Q_add(_v3_result)
                        else:
                            R_Q.inccount(_v3_result)

def _maint_R_Q_for__M_add(_elem):
    # Cost: O((_U_Q_bu + _U_Q_ub))
    #       O((_U_Q_bu + _U_Q_ub))
    (_v5_projects_python, _v5_p1) = _elem
    if hasfield(_v5_p1, 'developer'):
        _v5_p1_developer = _v5_p1.developer
        for _v5_projects_github in (_U_Q_bu[_v5_projects_python] if (_v5_projects_python in _U_Q_bu) else ()):
            if isset(_v5_projects_github):
                if (_v5_p1 in _v5_projects_github):
                    if ((_v5_projects_github, _v5_p1) != _elem):
                        _v5_result = (_v5_projects_python, _v5_projects_github, _v5_p1_developer)
                        if (_v5_result not in R_Q):
                            R_Q.add(_v5_result)
                            _maint_R_Q_bbu_for_R_Q_add(_v5_result)
                        else:
                            R_Q.inccount(_v5_result)
    (_v5_projects_github, _v5_p1) = _elem
    if hasfield(_v5_p1, 'developer'):
        _v5_p1_developer = _v5_p1.developer
        for _v5_projects_python in (_U_Q_ub[_v5_projects_github] if (_v5_projects_github in _U_Q_ub) else ()):
            if isset(_v5_projects_python):
                if (_v5_p1 in _v5_projects_python):
                    _v5_result = (_v5_projects_python, _v5_projects_github, _v5_p1_developer)
                    if (_v5_result not in R_Q):
                        R_Q.add(_v5_result)
                        _maint_R_Q_bbu_for_R_Q_add(_v5_result)
                    else:
                        R_Q.inccount(_v5_result)

def _demand_Q(_elem):
    # Cost: O(_v3_projects_python)
    #       O(_v3_projects_python)
    if (_elem not in _U_Q):
        _U_Q.add(_elem)
        _maint__U_Q_bu_for__U_Q_add(_elem)
        _maint__U_Q_ub_for__U_Q_add(_elem)
        _maint_R_Q_for__U_Q_add(_elem)



@app.route('/test')
def test():
    response = make_response('web')
    projects = Project.query.order_by(desc(Project.score)).all()

    projects_python = Set()
    projects_github = Set()
    for p in projects:
        if ('python' in map(strip, p.language.lower().split(','))):
            _v1 = (projects_python, p)
            index(_v1, 0).add(index(_v1, 1))
            _maint__M_ub_for__M_add(_v1)
            _maint_R_Q_for__M_add(_v1)
        if ('github' in p.home_page):
            _v2 = (projects_github, p)
            index(_v2, 0).add(index(_v2, 1))
            _maint__M_ub_for__M_add(_v2)
            _maint_R_Q_for__M_add(_v2)
    print(((_demand_Q((projects_python, projects_github)) or True) and (R_Q_bbu[(projects_python, projects_github)] if ((projects_python, projects_github) in R_Q_bbu) else Set())))

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
