import time
import json
from datetime import datetime
from .baseClass import BaseSlackFormartMessage


class DefaultSlackFormatMessage(BaseSlackFormartMessage):

    def __init__(self):
        self.template = {
            "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*{subject}*"
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "plain_text",
                                "text": "*CurrentTime* {nowtime}",
                                "emoji": True
                            },
                            {
                                "type": "plain_text",
                                "text": "*Timezone* {timezone}",
                                "emoji": True
                            }
                        ]
                    }
                ]
            }

    def validate(self):
        return True

    def format_message(self, message):
        if self.validate():
            subject = f"*{message}*"
            current_time = datetime.now().strftime("%Y-%m-%d:%H:%M")
            timezone = time.tzname[0]
            self.template["blocks"][0]["text"]["text"] = subject
            self.template["blocks"][1]["fields"][0]["text"] = current_time
            self.template["blocks"][1]["fields"][1]["text"] = timezone
            return self.template
        return None
