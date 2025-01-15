#!/usr/bin/python3
# Questions :
# {
#    "Survey_Name": {
#       "Page_Name": {
#           "Question1_Name": {
#               "Description" : "Description of question",
#               "Answers" : [
#                   "Answer1",
#                   "Answer2",
#                   "Answer3"
#               ]
#           },
#           "Question2_Name": {
#               "Description" : "Description of question",
#               "Answers" : [
#                   "Answer1",
#                   "Answer2",
#                   "Answer3"
#               ]
#           }
#           . . .
#       }
#    }
# }
# Users - as email from text file.
#
# .auth - contains bearer token for surveymonkey API
# credentials-sheets.json - for first time oauth generation for gmail
# token.json - generated after successfull first time login, used for auth from then on
#
# -s - for specifing survey from json
# -r - for specifing email addresses of users

""" Modules for parsing arguments and json files """
import argparse
import json
from os import path
import requests
import ezgmail

BASE = "https://api.surveymonkey.com/v3"
TIMEOUT = 10 # in secends
BEARER_TOKEN=""

def get(endpoint):
    """ Function for sending json get messeges """
    if not BEARER_TOKEN:
        raise ValueError('bearer_token')

    url = BASE + endpoint
    headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json', 
    'Authorization': f'Bearer {BEARER_TOKEN}'
    }
    r = requests.get(url, headers=headers, timeout=TIMEOUT)
    if r.status_code > 300:
        return {}
    return json.loads(r.text)

def post(payload, endpoint):
    """ Function for sending json post messeges """
    if not BEARER_TOKEN:
        raise ValueError('bearer_token')

    url = BASE + endpoint
    headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json', 
    'Authorization': f'Bearer {BEARER_TOKEN}'
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers, timeout=TIMEOUT)
    if r.status_code > 300:
        print(f'Error code: {r.status_code}, Endpoint: {endpoint}')
        return {}
    return json.loads(r.text)

def post_survey(survey_json):
    """ Function for sending survey on server """
    survey_title = list(survey_json.keys())[0]
    payload = {
        "title": survey_title,
        "nickname": survey_title,
        "buttons_text": {
        "next_button": "Next",
        "prev_button": "Prev",
        "exit_button": "Exit",
        "done_button": "Done"
        },
        "theme_id": 1506280,

        "pages": list(map(lambda page_title : {
            "title" : page_title,
            "questions": list(map(lambda question : {
                    "headings": [
                        {
                            "heading": \
                                survey_json[survey_title][page_title][question[1]]['Description'],
                        }
                    ],
                    "position": question[0]+1,
                    "family": "single_choice",
                    "subtype": "vertical",
                    "answers": {
                        "choices":
                            list(map(lambda x : { "text" : f"{x}" },\
                                    survey_json[survey_title][page_title][question[1]]['Answers'])),
                    }
                }
                , enumerate(list(survey_json[survey_title][page_title].keys()))))
        }, list(survey_json[survey_title].keys())))
    }
    res = post(payload, '/surveys')
    return res

def post_collectors_email(survey_id):
    """ Function for sending info about creation of collector """
    if survey_id is None:
        raise ValueError('survey_id')
    payload = {
        "type": "email"
    }
    res = post(payload, f'/surveys/{survey_id}/collectors')
    if not res:
        print("================== \
Creating collectors for email only with pro version. ===================")
    return res

def post_collectors_weblink(survey_id):
    """ Function for sending info about creation of collector """
    if survey_id is None:
        raise ValueError('survey_id')
    payload = {
        "type": "weblink"
    }
    res = post(payload, f'/surveys/{survey_id}/collectors')
    return res

def post_message(collector_id):
    """ Function for sending message text """
    if collector_id is None:
        raise ValueError('collector_id')
    payload = {
        "type": "invite"
    }
    res = post(payload, f'/collectors/{collector_id}/messages')
    return res

def post_reciepients(collector_id, message_id, emails_list):
    """ Function for sending group of reciepients to server """
    if collector_id is None:
        raise ValueError('collector_id')
    if message_id is None:
        raise ValueError('message_id')
    payload =  {
        "contacts": 
            list(map(lambda email : { "email": email }, emails_list))
    }
    res = post(payload, f'/collectors/{collector_id}/messages/{message_id}/recipients/bulk')
    return res

def post_send_surveys(collector_id, message_id):
    """ Function for sending requests to users """
    if collector_id is None:
        raise ValueError('collector_id')
    if message_id is None:
        raise ValueError('message_id')
    payload = {}
    res = post(payload, f'/collectors/{collector_id}/messages/{message_id}/send')
    return res


if __name__ ==  '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--recipients')
    parser.add_argument('-s', '--survey')

    args = parser.parse_args()
    try:
        with open(path.abspath('.auth'), 'r', encoding='utf-8') as f:
            BEARER_TOKEN=f.read().strip()
    except FileNotFoundError:
        print('Define .auth file with bearer token to survey monkey API in your working directory.')

    emails = []
    if args.recipients:
        with open(path.abspath(args.recipients), 'r', encoding='utf-8') as f:
            for line in f.readlines():
                unique = set()
                unique.add(line)
            emails = list(unique)
    survey = {}
    if args.survey:
        with open(path.abspath(args.survey), 'r', encoding='utf-8') as f:
            survey = json.load(f)
    try:
        if 'survey' not in locals():
            raise TypeError('survey', '-s')
        if  'emails' not in locals():
            raise TypeError('emails', '-r')
        resp = post_survey(survey)
        sm_survey_id = resp.get('id')
        resp = post_collectors_email(sm_survey_id)
        if resp :
            sm_collector_id = resp.get('id')
            resp = post_message(sm_collector_id)
            sm_message_id = resp.get('id')
            resp = post_reciepients(sm_collector_id, sm_message_id, emails)
            post_send_surveys(sm_collector_id, sm_message_id)
        else:
            conf = input('Do you want to use gmail? y/[n]')
            if conf == 'y':
                print("======== Proceeding =======")
                ezgmail.init()
                resp = post_collectors_weblink(sm_survey_id)
                weblink = resp['url']
                message = f"""
                    Hi, I am using gmail API to send surveymonkey surveys ;). 
                    It's part of python practical task.
                    Link to survey: {weblink}
                    """
                print('Would you like to send:')
                print(message)
                print('to:')
                for email in emails:
                    print(email)
                if input('y/[n]') == 'y':
                    for email in emails:
                        ezgmail.send(email, 'Python - Survey',
                             message)
    except TypeError as err:
        print(f'You need to specify: {err.args[0]} with {err.args[1]}')
    except ValueError as err:
        print(f'Empty: {err.args[0]}')
