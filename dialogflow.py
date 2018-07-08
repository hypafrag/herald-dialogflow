from dialogflow_v2 import SessionsClient
from subprocess import getoutput
from sys import argv
from os import environ as env
import config

env['GOOGLE_APPLICATION_CREDENTIALS'] = config.gc_credentials

sessions_client = SessionsClient()
session = sessions_client.session_path(config.gc_appid, config.session_name)
reply = sessions_client.detect_intent(session, {'text': {'text': ' '.join(argv[1:]), 'language_code': 'ru-RU'}})
result = reply.query_result
action = result.action

def play_poneys(where):
    getoutput("{}/.env/bin/python {}/skills.py play_poneys {}".format(
        config.herald_skills_path, config.herald_skills_path, where))

handlers = {
    'play_poneys': lambda parameters:
        play_poneys(parameters['where'])
}

if action in handlers:
    try:
        handlers[action](result.parameters)
    except OSError as ex:
        print('Ой')
        exit(ex.errno)

print(result.fulfillment_text)
exit(0)
