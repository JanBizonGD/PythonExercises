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

""" Modules for parsing arguments and json files """
import argparse
import json
from os import path
import requests

BASE = "https://api.surveymonkey.com/v3"
TIMEOUT = 10 # in secends


def get(endpoint):
    """ Function for sending json get messeges """
    url = BASE + endpoint
    headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json', 
    'Authorization': f'Bearer {bearer_token}'
    }
    r = requests.get(url, headers=headers, timeout=TIMEOUT)
    if r.status_code > 300:
        return {}
    return json.loads(r.text)

def post(payload, endpoint):
    """ Function for sending json post messeges """
    url = BASE + endpoint
    headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json', 
    'Authorization': f'Bearer {bearer_token}'
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers, timeout=TIMEOUT)
    if r.status_code > 300:
        print(f'Error code: {r.status_code}, Endpoint: {endpoint}')
        print(r.text)
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

def post_collectors(survey_id):
    """ Function for sending info about creation of collector """
    payload = {
        "type": "email"
    }
    res = post(payload, f'/surveys/{survey_id}/collectors')
    return res

def post_message(collector_id):
    """ Function for sending message text """
    payload = {
        "type": "invite"
    }
    res = post(payload, f'/collectors/{collector_id}/messages')
    return res

def post_reciepients(collector_id, message_id, emails):
    """ Function for sending group of reciepients to server """
    payload =  {
        "contacts": 
            list(map(lambda email : { "email": email }, emails))
    }
    res = post(payload, f'/collectors/{collector_id}/messages/{message_id}/recipients/bulk')
    return res

def post_send_surveys(collector_id, message_id):
    """ Function for sending requests to users """
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
            bearer_token=f.read().strip()
    except FileNotFoundError:
        print('Define .auth file with bearer token to survey monkey API in your working directory.')

    if args.recipients:
        with open(path.abspath(args.recipients), 'r', encoding='utf-8') as f:
            emails = []
            for line in f.readlines():
                emails.append(line)
    if args.survey:
        with open(path.abspath(args.survey), 'r', encoding='utf-8') as f:
            survey_json = json.load(f)
    try:
        if 'survey_json' not in locals():
            raise TypeError('survey_json', '-s')
        if  'emails' not in locals():
            raise TypeError('emails', '-r')
        res = post_survey(survey_json)
        res = post_collectors(res.get('id'))
        collector_id = res.get('id')
        if collector_id is not None:
            res = post_message(collector_id)
            message_id = res.get('id')
            if message_id is not None:
                res = post_reciepients(collector_id, message_id, emails)
                post_send_surveys(collector_id, message_id)
    except TypeError as err:
        print(f'You need to specify: {err.args[0]} with {err.args[1]}')

# TO DO : Paid feature.
