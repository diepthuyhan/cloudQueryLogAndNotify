import time
import json
from datetime import datetime
from .baseClass import BaseSlackFormartMessage


class DefaultSlackFormatMessage(BaseSlackFormartMessage):

    def __init__(self):
        self.template = {
                "attachments": [
                    {
                        "blocks": [
                            {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "*{subject}*"
                                }
                            },
                            {
                                "type": "context",
                                "elements": [
                                    {
                                        "type": "mrkdwn",
                                        "text": "*CurrentTime* {nowtime}"
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": "*Timezone* {timezone}"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }

    def validate(self):
        return True

    def format_message(self, message):
        if self.validate():
            if isinstance(message, dict):
                subject = json.dumps(message)
            else:
                subject = f"*{str(message)}*"
            current_time = f'*CurrentTime*: {datetime.now().strftime("%Y-%m-%d:%H:%M")}'
            timezone = f"*Timezone* {time.tzname[0]}"
            self.template["attachments"][0]["blocks"][0]["text"]["text"] = subject
            self.template["attachments"][0]["blocks"][1]["elements"][0]["text"] = current_time
            self.template["attachments"][0]["blocks"][1]["elements"][1]["text"] = timezone
            return self.template
        return None

