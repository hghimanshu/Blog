from classifier import app
import json
import sys
# sys.path.append('/home/techject/Abhishek/C3-python/')
import os
import flask
import time
import random
from flask import render_template

# @app.route("/UploadSet",methods=["POST"])
# def UploadSet():
#     flask_requests = flask.request.form.to_dict(flat=False) 
#     data={'Message': 'Data not uploaded!!'}
#     if flask.request.method == 'POST':
#         print(flask_requests)
#         server_name = flask_requests['serverName'][0]
#         set_list = flask_requests['set_list']
#         set_list = set_list[0].split(',')
#         set_list = [i.replace(' ', '') for i in set_list ]
#         is_sample = flask_requests['isSample'][0]
#         required_votes = flask_requests['requiredVotes'][0]
#         threshold_votes = flask_requests['thresholdVotes'][0]
#         work_flow_name = flask_requests['workFlowName'][0]
#         question = flask_requests['question'][0]
#         user_id = flask_requests['userId'][0]
#         user_name = flask_requests['userName'][0]

#         response = check_set_state(server_name, set_list, is_sample, work_flow_name, 
#                                 required_votes, threshold_votes, question, 
#                                 user_id, user_name)

#         print(response)
#     return flask.redirect('/admin')


# @app.route("/fetching_sets")
# def fetching_sets():
#     data={"success":False}
#     data={"sets":''}
#     status = False
#     sets = fetch_unuploaded_sets(status)
#     data['sets']=sets
#     data['success'] = True
#     return flask.jsonify(data)


@app.route('/testing')
def testing():
    return render_template('home.html')
