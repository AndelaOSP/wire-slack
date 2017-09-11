import json
import re
import datetime, time
import requests
from slackbot.bot import respond_to, default_reply

INCIDENT_DATA = {
    'category_id': 1,
    'location_id': 1,
    'description': '',
    'date_occurred': ''
}

RED_FLAG = \
"""
- Frequent office absence without authorization.\n
- Use of abusive language\n
- Theft \n
- Fraud """

YELLOW_FLAG = \
"""
- Bad attitude towards colleagues e.g. Rumor mill, laziness, uncollaborative \n
- Taking extended leave days without prior notification and approval from your Line manager \n
- Excessive tardiness \n
- Disrespect of colleagues space and/or beliefs (especially after consistent feedback) \n
"""

GREEN_FLAG = \
"""
- Not following the laid down procedures or not listening to instructions thus end up committing errors. \n
- Improper use of work tools and equipments. \n
"""


@respond_to('log incident', re.IGNORECASE)
def log(message):
    guide = [
        {
            "fallback": "",
            "fields": [
                {
                    "title": "Red",
                    "value": RED_FLAG,
                    "short": False
                },
                {
                    "title": "Yellow",
                    "value": YELLOW_FLAG,
                    "short": False
                },
                {
                    "title": "Green",
                    "value": GREEN_FLAG,
                    "short": False
                }
            ],
            "color": "#3359DF"
        }
    ]
    print(message.body)
    message.reply_webapi('What Type of incident would you like to report?', json.dumps(guide))

@respond_to('(red)|(yellow)|(green)', re.IGNORECASE)
def incident_category(message, red, yellow, green):
    ct = red or yellow or green
    INCIDENT_DATA['date_occurred'] = datetime.datetime.now().__str__()
    message.reply("Tell me about the incident")

@default_reply
def incidet_description(message):
    print(message)
    if INCIDENT_DATA['date_occurred'] != '':
        INCIDENT_DATA['description'] = message.body['text']
        print(INCIDENT_DATA)
        r = requests.post('http://app.nairobi.us/wire/api/incidents', data = INCIDENT_DATA)
        if r.status_code == 200:
            message.reply('Incident logged')
    else:
        message.reply('I did not understand that')
        log(message)
