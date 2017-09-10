import json
import re
from slackbot.bot import respond_to, listen_to

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

@respond_to('(red|yellow|green)', re.IGNORECASE)
def category(message):
    message.reply("Tell me about the incident")
    