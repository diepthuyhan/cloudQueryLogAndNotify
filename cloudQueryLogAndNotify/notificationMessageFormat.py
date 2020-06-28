import time
from datetime import datetime
from .baseClass import BaseSlackFormartMessage


class DefaultSlackFormatMessage(BaseSlackFormartMessage):

    def __init__(self):
        self.template = '''{
            "attachments": [
                {
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "{subject}"
                            }
                        },
                        {
                            "type": "section",
                            "fields": [
                                {
                                    "type": "plain_text",
                                    "text": "*CurrentTime* {nowtime}",
                                    "emoji": true
                                },
                                {
                                    "type": "plain_text",
                                    "text": "*Timezone* {timezone}",
                                    "emoji": true
                                }
                            ]
                        }
                    ]
                }
            ]
        }'''

    def format_message(self, message):
        if self.validate():
            return self.template.format(
                subject=message,
                nowtime=datetime.now().strftime("%Y-%m-%d:%H:%M"),
                timezone=time.tzname[0]
            )
        return None
